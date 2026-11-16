
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.models.stock_price import StockPrice

from app.ml.data.clean_data import clean_stock_data
from app.ml.features.build_features import build_features

from app.ml.data.prepare_dataset import FEATURE_COLUMNS
from app.ml.models.model_loader import get_prediction_model


SUPPORTED_SYMBOLS = {
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
}

HISTORY_LIMIT = 250


def predict_stock_return(
    db: Session,
    symbol: str
) -> dict:

    symbol = symbol.strip().upper()

    if symbol not in SUPPORTED_SYMBOLS:
        raise ValueError(
            f"Unsupported stock symbol: {symbol}"
        )

    # 1. Find stock in database
    stock = (
        db.query(Stock)
        .filter(Stock.symbol == symbol)
        .first()
    )

    if stock is None:
        raise ValueError(
            f"Stock {symbol} not found in database"
        )

    # 2. Fetch latest historical prices
    records = (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock.id)
        .order_by(StockPrice.date.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )

    if len(records) < 30:
        raise ValueError(
            f"Insufficient historical data for {symbol}. "
            "At least 30 records are required."
        )

    # 3. Convert database records to DataFrame
    records.reverse()

    df = pd.DataFrame([
        {
            "date": record.date,
            "open": record.open,
            "high": record.high,
            "low": record.low,
            "close": record.close,
            "volume": record.volume,
        }
        for record in records
    ])

    # 4. Clean historical data
    df = clean_stock_data(df)

    if len(df) < 30:
        raise ValueError(
            f"Insufficient valid historical data for {symbol}"
        )

    # 5. Generate the same features used during training
    feature_df = build_features(
        df,
        include_target=False
    )

    if feature_df.empty:
        raise ValueError(
            f"Unable to generate features for {symbol}"
        )

    # 6. Select latest available feature row
    latest_row = feature_df.iloc[-1]

    X = feature_df.loc[
        [feature_df.index[-1]],
        FEATURE_COLUMNS
    ]

    # 7. Validate feature values
    if not np.isfinite(X.to_numpy(dtype=float)).all():
        raise ValueError(
            "Invalid feature values generated"
        )

    # 8. Load stock-specific return model
    model_name = f"{symbol.lower()}_return"

    model = get_prediction_model(
        model_name=model_name,
        version="v1"
    )

    # 9. Predict next-day percentage return
    predicted_return = float(
        model.predict(X)[0]
    )

    if not np.isfinite(predicted_return):
        raise ValueError(
            "Model generated an invalid prediction"
        )

    return {
        "symbol": symbol,
        "company_name": stock.company_name,
        "last_available_date": latest_row["date"],
        "current_close": float(latest_row["close"]),
        "predicted_return": predicted_return,
        "predicted_return_percent": predicted_return * 100,
        "model_name": model_name,
        "model_version": "v1",
        "prediction_horizon": "Next available trading day",
        "generated_at": datetime.now(timezone.utc),
    }
