
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.db.database import SessionLocal
from app.ml.data.load_data import load_stock_data
from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features
from app.ml.data.prepare_dataset import prepare_train_test_data


def evaluate_baseline(symbol: str):

    db = SessionLocal()

    try:
        df = load_stock_data(db, symbol)
        df = clean_stock_data(df)
        df = build_features(df)

        # Keep the same chronological order as the split function
        df = df.sort_values("date").reset_index(drop=True)

        X_train, X_test, y_train, y_test = prepare_train_test_data(df)

        # Get test dates using the same chronological split boundary
        unique_dates = sorted(df["date"].unique())
        split_index = int(len(unique_dates) * 0.8)
        test_dates = unique_dates[split_index:]

        test_df = df[df["date"].isin(test_dates)]

        # Naive baseline: today's close predicts next day's close
        predictions = test_df["close"].values

        assert len(predictions) == len(y_test), (
            "Prediction and target lengths do not match"
        )

        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        print("\nNaive Baseline Evaluation")
        print("Stock:", symbol)
        print("Training rows:", len(X_train))
        print("Testing rows:", len(X_test))
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2 Score: {r2:.4f}")

    finally:
        db.close()


if __name__ == "__main__":
    evaluate_baseline("RELIANCE")
