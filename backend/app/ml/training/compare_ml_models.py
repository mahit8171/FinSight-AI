
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    HistGradientBoostingRegressor
)
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.ml.data.prepare_walk_forward_split import (
    prepare_walk_forward_split
)


TOP_FEATURES = [
    "high_ratio",
    "open_ratio",
    "volume_change",
    "low_ratio",
    "volatility_5",
]


def prepare_data(X_train, X_test):

    X_train = X_train[TOP_FEATURES + ["symbol"]].copy()
    X_test = X_test[TOP_FEATURES + ["symbol"]].copy()

    X_train = pd.get_dummies(
        X_train,
        columns=["symbol"],
        dtype=int
    )

    X_test = pd.get_dummies(
        X_test,
        columns=["symbol"],
        dtype=int
    )

    X_test = X_test.reindex(
        columns=X_train.columns,
        fill_value=0
    )

    return X_train, X_test


def evaluate_model(model, X_train, X_test, y_train, y_test):

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    return mae, rmse


def compare_models():

    folds = prepare_walk_forward_split()

    results = []

    for fold_number, (X_train, X_test, y_train, y_test) in enumerate(
        folds, start=1
    ):

        X_train, X_test = prepare_data(X_train, X_test)

        models = {
            "Linear Regression": LinearRegression(),

            "Random Forest": RandomForestRegressor(
                n_estimators=200,
                max_depth=5,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            ),

            "Gradient Boosting": HistGradientBoostingRegressor(
                max_iter=100,
                learning_rate=0.05,
                max_leaf_nodes=15,
                l2_regularization=1,
                random_state=42
            )
        }

        for model_name, model in models.items():

            mae, rmse = evaluate_model(
                model,
                X_train,
                X_test,
                y_train,
                y_test
            )

            results.append({
                "Fold": fold_number,
                "Model": model_name,
                "MAE": mae,
                "RMSE": rmse
            })

        baseline = [0.0] * len(y_test)

        results.append({
            "Fold": fold_number,
            "Model": "Zero Return Baseline",
            "MAE": mean_absolute_error(y_test, baseline),
            "RMSE": mean_squared_error(y_test, baseline) ** 0.5
        })

    results_df = pd.DataFrame(results)

    print("\nModel Comparison - Top 5 Features")
    print("=" * 65)

    print(results_df.to_string(index=False))

    print("\nAverage Performance")
    print("=" * 65)

    summary = (
        results_df.groupby("Model")[["MAE", "RMSE"]]
        .mean()
        .sort_values("MAE")
    )

    print(summary.to_string())


if __name__ == "__main__":
    compare_models()
