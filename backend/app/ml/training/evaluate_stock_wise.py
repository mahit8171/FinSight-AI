
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

from app.ml.data.prepare_multi_stock_split import prepare_multi_stock_split
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def evaluate_stock_wise():
    X_train, X_test, y_train, y_test = prepare_multi_stock_split()

    preprocessor = pd.get_dummies(
        X_train["symbol"],
        prefix="stock"
    )

    X_train_encoded = pd.concat(
        [
            X_train[FEATURE_COLUMNS].reset_index(drop=True),
            preprocessor.reset_index(drop=True),
        ],
        axis=1,
    )

    X_test_encoded = pd.concat(
        [
            X_test[FEATURE_COLUMNS].reset_index(drop=True),
            pd.get_dummies(
                X_test["symbol"],
                prefix="stock"
            ).reindex(
                columns=preprocessor.columns,
                fill_value=0
            ).reset_index(drop=True),
        ],
        axis=1,
    )

    model = LinearRegression()
    model.fit(X_train_encoded, y_train)

    predictions = model.predict(X_test_encoded)

    results = pd.DataFrame({
        "symbol": X_test["symbol"].values,
        "actual": y_test.values,
        "predicted": predictions,
        "baseline": 0.0,
    })

    print("\nStock-wise Model Performance")
    print("----------------------------")

    for symbol, group in results.groupby("symbol"):
        mae = mean_absolute_error(group["actual"], group["predicted"])
        rmse = np.sqrt(
            mean_squared_error(group["actual"], group["predicted"])
        )

        baseline_mae = mean_absolute_error(
            group["actual"],
            group["baseline"]
        )

        print(f"\n{symbol}")
        print(f"Model MAE:    {mae:.6f}")
        print(f"Baseline MAE: {baseline_mae:.6f}")
        print(f"RMSE:         {rmse:.6f}")


if __name__ == "__main__":
    evaluate_stock_wise()
