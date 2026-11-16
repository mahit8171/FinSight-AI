
from pathlib import Path

import yaml
import mlflow
import mlflow.sklearn
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from app.ml.data.prepare_dvc_dataset import prepare_dvc_dataset
from app.ml.data.prepare_dvc_split import split_stock_data
from app.ml.models.model_registry import save_model


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[4]

PARAMS_PATH = PROJECT_ROOT / "params.yaml"
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"

TRACKING_URI = (
    f"sqlite:///{MLFLOW_DB_PATH.as_posix()}"
)


def load_params():
    if not PARAMS_PATH.exists():
        raise FileNotFoundError(
            f"params.yaml not found: {PARAMS_PATH}"
        )

    with open(PARAMS_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def train_all_models():

    params = load_params()

    stocks = params["stocks"]
    training_config = params["training"]
    mlflow_config = params["mlflow"]

    model_type = training_config["model_type"]
    test_size = float(training_config["test_size"])
    target = training_config["target"]

    if target != "target_return":
        raise ValueError(
            "This pipeline currently supports target_return only"
        )

    if model_type != "LinearRegression":
        raise ValueError(
            f"Unsupported model type: {model_type}"
        )

    # Local MLflow tracking
    # SQLite-based MLflow tracking
    mlflow.set_tracking_uri(TRACKING_URI)

   

    mlflow.set_experiment(
        mlflow_config["experiment_name"]
    )

    print("\nPreparing DVC dataset...")

    df = prepare_dvc_dataset(symbols=stocks)

    results = []

    for symbol, stock_df in df.groupby("symbol"):

        print(f"\nTraining model for {symbol}")
        print("=" * 45)

        X_train, X_test, y_train, y_test = split_stock_data(
            stock_df,
            test_size=test_size,
        )

        model = LinearRegression()

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Zero-return baseline
        baseline_predictions = np.zeros(len(y_test))

        metrics = {
            "mae": float(
                mean_absolute_error(y_test, predictions)
            ),
            "rmse": float(
                np.sqrt(
                    mean_squared_error(y_test, predictions)
                )
            ),
            "r2": float(
                r2_score(y_test, predictions)
            ),
            "baseline_mae": float(
                mean_absolute_error(
                    y_test,
                    baseline_predictions,
                )
            ),
            "baseline_rmse": float(
                np.sqrt(
                    mean_squared_error(
                        y_test,
                        baseline_predictions,
                    )
                )
            ),
        }

        model_name = f"{symbol.lower()}_return"

        # Save model in existing joblib registry
        model_path = save_model(
            model=model,
            model_name=model_name,
            version="v1",
        )

        # One independent MLflow run per stock
        with mlflow.start_run(
            run_name=f"{symbol}_LinearRegression"
        ):

            mlflow.set_tags({
                "stock_symbol": symbol,
                "model_type": model_type,
                "prediction_target": target,
            })

            mlflow.log_params({
                "stock": symbol,
                "model_type": model_type,
                "test_size": test_size,
                "target": target,
                "training_rows": len(X_train),
                "testing_rows": len(X_test),
                "feature_count": X_train.shape[1],
            })

            mlflow.log_metrics(metrics)

            # Log trained model to MLflow
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
            )

            # Log the existing joblib artifact too
            mlflow.log_artifact(str(model_path))

        results.append({
            "symbol": symbol,
            **metrics,
        })

        print("Training rows:", len(X_train))
        print("Testing rows:", len(X_test))

        for metric_name, metric_value in metrics.items():
            print(f"{metric_name}: {metric_value:.6f}")

    print("\nAll stock models trained successfully.")
    print("\nFinal Results:")

    for result in results:
        print(result)

    print("\nMLflow database:", MLFLOW_DB_PATH)


if __name__ == "__main__":
    train_all_models()
