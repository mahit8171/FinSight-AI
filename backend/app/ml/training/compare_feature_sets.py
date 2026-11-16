
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.ml.data.prepare_walk_forward_split import prepare_walk_forward_split
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


# Original 9 features
OLD_FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "volatility_5",
    "volume_change",
    "open_ratio",
    "high_ratio",
    "low_ratio",
    "sma5_ratio",
    "sma10_ratio",
]

# Updated 15 features
NEW_FEATURE_COLUMNS = FEATURE_COLUMNS


def evaluate_model(X_train, X_test, y_train, y_test, features):

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "symbol",
                OneHotEncoder(handle_unknown="ignore"),
                ["symbol"],
            ),
            (
                "features",
                "passthrough",
                features,
            ),
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

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    return mae, rmse


def compare_feature_sets():

    # Generate folds only once for a fair comparison
    folds = prepare_walk_forward_split()

    results = []

    for fold_number, (X_train, X_test, y_train, y_test) in enumerate(
        folds, start=1
    ):

        # Model A: Original 9 features
        old_mae, old_rmse = evaluate_model(
            X_train,
            X_test,
            y_train,
            y_test,
            OLD_FEATURE_COLUMNS,
        )

        # Model B: Updated 15 features
        new_mae, new_rmse = evaluate_model(
            X_train,
            X_test,
            y_train,
            y_test,
            NEW_FEATURE_COLUMNS,
        )

        # Zero-return baseline
        baseline_predictions = np.zeros(len(y_test))

        baseline_mae = mean_absolute_error(
            y_test,
            baseline_predictions,
        )

        baseline_rmse = np.sqrt(
            mean_squared_error(
                y_test,
                baseline_predictions,
            )
        )

        results.append({
            "fold": fold_number,
            "old_mae": old_mae,
            "new_mae": new_mae,
            "baseline_mae": baseline_mae,
            "old_rmse": old_rmse,
            "new_rmse": new_rmse,
            "baseline_rmse": baseline_rmse,
        })

        print(f"\nFold {fold_number}")
        print("----------------------------")
        print(f"Old 9 Features MAE: {old_mae:.6f}")
        print(f"New 15 Features MAE: {new_mae:.6f}")
        print(f"Baseline MAE: {baseline_mae:.6f}")

        print(f"Old 9 Features RMSE: {old_rmse:.6f}")
        print(f"New 15 Features RMSE: {new_rmse:.6f}")
        print(f"Baseline RMSE: {baseline_rmse:.6f}")

    results_df = pd.DataFrame(results)

    print("\nAverage Controlled Experiment Results")
    print("-------------------------------------")

    print(
        results_df.drop(columns=["fold"])
        .mean()
        .to_string()
    )


if __name__ == "__main__":
    compare_feature_sets()
