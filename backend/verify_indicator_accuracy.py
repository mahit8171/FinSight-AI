
import requests
import pandas as pd
import numpy as np

from math import sqrt
from app.db.database import SessionLocal
from app.models.stock import Stock
from app.models.stock_price import StockPrice


SYMBOL = "RELIANCE"
API_URL = f"http://127.0.0.1:8000/api/v1/stocks/{SYMBOL}/analytics"


db = SessionLocal()

try:
    # 1. Fetch raw closing prices directly from PostgreSQL
    stock = db.query(Stock).filter(
        Stock.symbol == SYMBOL
    ).first()

    if not stock:
        raise ValueError("Stock not found")

    records = (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock.id)
        .order_by(StockPrice.date.asc())
        .all()
    )

    raw = pd.DataFrame([
        {"date": r.date.isoformat(), "close": r.close}
        for r in records
    ])

finally:
    db.close()


# 2. Fetch actual Analytics API response
response = requests.get(API_URL, params={"limit": 1000})
response.raise_for_status()

api_data = response.json()["data"]
api_df = pd.DataFrame(api_data)

if len(raw) != len(api_df):
    raise ValueError(
        f"Record count mismatch: DB={len(raw)}, API={len(api_df)}"
    )


# 3. Independent calculations from raw closing prices
close = raw["close"].astype(float)

expected = pd.DataFrame(index=raw.index)
expected["daily_returns"] = close.pct_change() * 100

expected["sma_20"] = close.rolling(
    window=20, min_periods=20
).mean()

expected["sma_50"] = close.rolling(
    window=50, min_periods=50
).mean()

expected["ema_20"] = close.ewm(
    span=20, adjust=False, min_periods=20
).mean()


# RSI 14
delta = close.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.ewm(
    alpha=1/14, adjust=False, min_periods=14
).mean()

avg_loss = loss.ewm(
    alpha=1/14, adjust=False, min_periods=14
).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

rsi = rsi.mask((avg_loss == 0) & (avg_gain > 0), 100)
rsi = rsi.mask((avg_gain == 0) & (avg_loss > 0), 0)
rsi = rsi.mask((avg_gain == 0) & (avg_loss == 0), 50)

expected["rsi_14"] = rsi


# Annualized volatility 20
daily_returns = close.pct_change()

expected["volatility_20"] = (
    daily_returns.rolling(20, min_periods=20).std()
    * sqrt(252) * 100
)


# MACD 12, 26, 9
ema_fast = close.ewm(
    span=12, adjust=False, min_periods=12
).mean()

ema_slow = close.ewm(
    span=26, adjust=False, min_periods=26
).mean()

expected["macd"] = ema_fast - ema_slow

expected["signal"] = expected["macd"].ewm(
    span=9, adjust=False, min_periods=9
).mean()

expected["histogram"] = (
    expected["macd"] - expected["signal"]
)


# 4. Compare independent results with API results
columns = [
    "daily_returns",
    "sma_20",
    "sma_50",
    "ema_20",
    "rsi_14",
    "volatility_20",
    "macd",
    "signal",
    "histogram"
]

print("\n========== INDICATOR ACCURACY REPORT ==========\n")

for column in columns:
    actual = pd.to_numeric(
        api_df[column], errors="coerce"
    ).to_numpy(dtype=float)

    calculated = expected[column].to_numpy(dtype=float)

    null_match = np.isnan(actual) == np.isnan(calculated)

    numeric_match = np.isclose(
        actual, calculated,
        rtol=1e-8,
        atol=1e-8,
        equal_nan=True
    )

    passed = bool(np.all(null_match & numeric_match))

    print(f"{column}: {'PASS' if passed else 'FAIL'}")

    if not passed:
        mismatch_indices = np.where(
            ~(null_match & numeric_match)
        )[0]

        for index in mismatch_indices[:5]:
            print(
                f"  Row {index + 1}: "
                f"API={actual[index]}, "
                f"Expected={calculated[index]}"
            )

print("\n========== VERIFICATION COMPLETED ==========")
