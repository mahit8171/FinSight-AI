
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.ml.data.prepare_walk_forward_split import (
    prepare_walk_forward_split
)
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


TOP_FEATURES = [
    "high_ratio",
    "open_ratio",
    "volume_change",
    "low_ratio",
    "volatility_5",
]


def evaluate_features(X_train, X_test, y_train, y_test):

    X_train = pd.get_dummies(
        X_train.copy(),
        columns=["symbol"],
        dtype=int
    )

    X_test = pd.get_dummies(
        X_test.copy(),
        columns=["symbol"],
        dtype=int
    )

    X_test = X_test.reindex(
        columns=X_train.columns,
        fill_value=0
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    return mae, rmse


def compare_feature_selection():

    folds = prepare_walk_forward_split()

    results = []

    for fold_number, (X_train, X_test, y_train, y_test) in enumerate(
        folds, start=1
    ):

        # Experiment A: All 15 features
        all_train = X_train[FEATURE_COLUMNS + ["symbol"]]
        all_test = X_test[FEATURE_COLUMNS + ["symbol"]]

        all_mae, all_rmse = evaluate_features(
            all_train,
            all_test,
            y_train,
            y_test
        )

        # Experiment B: Top 5 features
        top_train = X_train[TOP_FEATURES + ["symbol"]]
        top_test = X_test[TOP_FEATURES + ["symbol"]]

        top_mae, top_rmse = evaluate_features(
            top_train,
            top_test,
            y_train,
            y_test
        )

        # Baseline: Predict zero return
        baseline = [0.0] * len(y_test)

        baseline_mae = mean_absolute_error(
            y_test,
            baseline
        )

        baseline_rmse = (
            mean_squared_error(y_test, baseline) ** 0.5
        )

        results.append({
            "Fold": fold_number,
            "All 15 MAE": all_mae,
            "Top 5 MAE": top_mae,
            "Baseline MAE": baseline_mae,
            "All 15 RMSE": all_rmse,
            "Top 5 RMSE": top_rmse,
            "Baseline RMSE": baseline_rmse,
        })

    results_df = pd.DataFrame(results)

    print("\nFeature Selection Comparison")
    print("=" * 90)
    print(results_df.to_string(index=False))

    print("\nAverage Performance")
    print("=" * 90)
    print(
        results_df.drop(columns=["Fold"])
        .mean()
        .to_string()
    )


if __name__ == "__main__":
    compare_feature_selection()
