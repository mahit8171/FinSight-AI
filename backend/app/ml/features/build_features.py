
import numpy as np
import pandas as pd


def build_features(
    df: pd.DataFrame,
    include_target: bool = True
) -> pd.DataFrame:
    """
    Build technical and relative price features for stock prediction.
    Input must contain one stock's chronological historical data.
    """

    df = df.copy()
    df = df.sort_values("date").reset_index(drop=True)

    # Daily returns
    df["return_1d"] = df["close"].pct_change()
    df["return_5d"] = df["close"].pct_change(5)

    # Moving averages
    df["sma_5"] = df["close"].rolling(window=5).mean()
    df["sma_10"] = df["close"].rolling(window=10).mean()

    # Exponential moving average
    df["ema_20"] = df["close"].ewm(
        span=20,
        adjust=False
    ).mean()

    # Rolling volatility
    df["volatility_5"] = (
        df["return_1d"].rolling(window=5).std()
    )

    # Volume percentage change
    df["volume_change"] = df["volume"].pct_change()

    # RSI (14)
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / 14,
        adjust=False,
        min_periods=14
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / 14,
        adjust=False,
        min_periods=14
    ).mean()

 
    # Calculate RSI safely
    rs = avg_gain / avg_loss.replace(0, np.nan)

    rsi = 100 - (100 / (1 + rs))

    # If average loss is zero but average gain is positive,
    # RSI should be 100.
    rsi = rsi.mask(
        (avg_loss == 0) & (avg_gain > 0),
        100
    )

    # If both average gain and average loss are zero,
    # RSI should be 50.
    rsi = rsi.mask(
        (avg_gain == 0) & (avg_loss == 0),
        50
    )

    df["rsi_14"] = rsi


    # MACD (12, 26, 9)
    ema_12 = df["close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema_26 = df["close"].ewm(
        span=26,
        adjust=False
    ).mean()

    df["macd"] = ema_12 - ema_26

    macd_signal = df["macd"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["macd_histogram"] = df["macd"] - macd_signal

    # Momentum (10)
    df["momentum_10"] = df["close"].pct_change(10)

    # Bollinger Bands (20, 2)
    sma_20 = df["close"].rolling(window=20).mean()
    std_20 = df["close"].rolling(window=20).std()

    upper_band = sma_20 + (2 * std_20)
    lower_band = sma_20 - (2 * std_20)

    # Relative Bollinger Band position
    band_width = upper_band - lower_band

    df["bb_position"] = (
        (df["close"] - lower_band) /
        band_width.replace(0, np.nan)
    )

    # Relative price features
    previous_close = df["close"].shift(1)

    df["open_ratio"] = df["open"] / previous_close
    df["high_ratio"] = df["high"] / previous_close
    df["low_ratio"] = df["low"] / previous_close

    df["sma5_ratio"] = df["sma_5"] / df["close"]
    df["sma10_ratio"] = df["sma_10"] / df["close"]
    df["ema20_ratio"] = df["ema_20"] / df["close"]

    # Next trading day's target
    # Next trading day's target (training only)
    if include_target:
        df["target_date"] = df["date"].shift(-1)
        df["target"] = df["close"].shift(-1)

    # Replace infinite values
    df = df.replace([np.inf, -np.inf], np.nan)

    # Ensure numeric volume feature
    df["volume_change"] = pd.to_numeric(
        df["volume_change"],
        errors="coerce"
    )

   
    # Remove invalid rows
    if include_target:
        df = df.dropna().reset_index(drop=True)

    else:
        from app.ml.data.prepare_dataset import FEATURE_COLUMNS

        df = df.dropna(
            subset=FEATURE_COLUMNS
        ).reset_index(drop=True)

    return df