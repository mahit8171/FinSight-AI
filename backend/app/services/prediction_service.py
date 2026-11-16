
from app.db.database import SessionLocal

from app.ml.data.load_data import load_stock_data
from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features
from app.ml.data.prepare_dataset import FEATURE_COLUMNS
from app.ml.models.model_loader import get_prediction_model


def predict_stock_price(symbol: str):
    """
    Generate next-day stock closing price prediction.
    Currently supports RELIANCE only.
    """

    symbol = symbol.upper().strip()

    if symbol != "RELIANCE":
        raise ValueError(
            "Currently prediction is available only for RELIANCE"
        )

    db = SessionLocal()

    try:
        # 1. Load historical stock data
        df = load_stock_data(db, symbol)

        if df.empty:
            raise ValueError(f"No historical data found for {symbol}")

        # 2. Clean data
        df = clean_stock_data(df)

        # 3. Build features
        df = build_features(df)

        if df.empty:
            raise ValueError("Not enough data to generate features")

        # 4. Get latest feature row
        latest_row = df.sort_values("date").iloc[-1]

        X_latest = latest_row[FEATURE_COLUMNS].to_frame().T

        # 5. Load trained model
        model = get_prediction_model(
            model_name="reliance_linear_regression",
            version="v1"
        )

        # 6. Generate prediction
        predicted_price = float(model.predict(X_latest)[0])

        current_price = float(latest_row["close"])

        # 7. Calculate predicted change
        predicted_change = predicted_price - current_price

        predicted_change_percent = (
            predicted_change / current_price
        ) * 100 if current_price else 0

        return {
            "symbol": symbol,
            "last_available_date": latest_row["date"],
            "current_close": current_price,
            "predicted_next_close": predicted_price,
            "predicted_change": predicted_change,
            "predicted_change_percent": predicted_change_percent,
            "model_name": "linear_regression",
            "model_version": "v1"
        }

    finally:
        db.close()
