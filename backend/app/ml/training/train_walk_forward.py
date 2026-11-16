
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.ml.data.prepare_walk_forward_split import prepare_walk_forward_split
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def train_walk_forward():

    folds = prepare_walk_forward_split()

    results = []

    for fold_number, (X_train, X_test, y_train, y_test) in enumerate(folds, start=1):

        preprocessor = ColumnTransformer(
            transformers=[
                ("symbol", OneHotEncoder(handle_unknown="ignore"), ["symbol"]),
                ("features", "passthrough", FEATURE_COLUMNS),
            ]
        )

        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("regressor", LinearRegression()),
            ]
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        baseline_predictions = np.zeros(len(y_test))

        model_mae = mean_absolute_error(y_test, predictions)
        model_rmse = np.sqrt(mean_squared_error(y_test, predictions))

        baseline_mae = mean_absolute_error(y_test, baseline_predictions)
        baseline_rmse = np.sqrt(
            mean_squared_error(y_test, baseline_predictions)
        )

        results.append({
            "fold": fold_number,
            "model_mae": model_mae,
            "model_rmse": model_rmse,
            "baseline_mae": baseline_mae,
            "baseline_rmse": baseline_rmse,
        })

        print(f"\nFold {fold_number} Results")
        print("--------------------")
        print(f"Model MAE:       {model_mae:.6f}")
        print(f"Model RMSE:      {model_rmse:.6f}")
        print(f"Baseline MAE:    {baseline_mae:.6f}")
        print(f"Baseline RMSE:   {baseline_rmse:.6f}")

    results_df = pd.DataFrame(results)

    print("\nAverage Walk-Forward Results")
    print("----------------------------")
    print(results_df.mean(numeric_only=True).to_string())


if __name__ == "__main__":
    train_walk_forward()
