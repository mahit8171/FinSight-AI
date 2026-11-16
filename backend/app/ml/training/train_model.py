
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from app.db.database import SessionLocal
from app.ml.data.load_data import load_stock_data
from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features
from app.ml.data.prepare_dataset import prepare_train_test_data
from app.ml.models.model_registry import save_model


def train_linear_regression(symbol: str):

    db = SessionLocal()

    try:
        df = load_stock_data(db, symbol)
        df = clean_stock_data(df)
        df = build_features(df)

        X_train, X_test, y_train, y_test = prepare_train_test_data(df)

        # Scaling + Linear Regression
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", LinearRegression()),
        ])

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        print("\nScaled Linear Regression Evaluation")
        print("Stock:", symbol)
        print("Training samples:", len(X_train))
        print("Testing samples:", len(X_test))
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2 Score: {r2:.4f}")

        print("First 5 predictions:", predictions[:5])
        print("First 5 actual values:", y_test.iloc[:5].values)
        
        save_model(
        model,
        model_name=f"{symbol.lower()}_linear_regression",
        version="v1"
         )

        return model

    finally:
        db.close()


if __name__ == "__main__":
    train_linear_regression("RELIANCE")
