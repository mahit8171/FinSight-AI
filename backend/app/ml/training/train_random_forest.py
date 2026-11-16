
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from app.db.database import SessionLocal
from app.ml.data.load_data import load_stock_data
from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features
from app.ml.data.prepare_dataset import prepare_train_test_data


def train_random_forest(symbol: str):

    db = SessionLocal()

    try:
        df = load_stock_data(db, symbol)
        df = clean_stock_data(df)
        df = build_features(df)

        X_train, X_test, y_train, y_test = prepare_train_test_data(df)

        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        print("\nRandom Forest Evaluation")
        print("Stock:", symbol)
        print("Training samples:", len(X_train))
        print("Testing samples:", len(X_test))
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2 Score: {r2:.4f}")

        return model

    finally:
        db.close()


if __name__ == "__main__":
    train_random_forest("RELIANCE")
