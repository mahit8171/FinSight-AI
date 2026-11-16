
import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.data.prepare_multi_stock_split import prepare_multi_stock_split


def evaluate_baseline():
    X_train, X_test, y_train, y_test = prepare_multi_stock_split()

    predictions = np.zeros(len(y_test))

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\nZero Return Baseline Results")
    print("----------------------------")
    print("Testing samples:", len(y_test))
    print(f"MAE: {mae:.6f}")
    print(f"RMSE: {rmse:.6f}")
    print(f"R2 Score: {r2:.6f}")


if __name__ == "__main__":
    evaluate_baseline()
