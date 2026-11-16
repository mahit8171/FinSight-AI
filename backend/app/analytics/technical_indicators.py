
import pandas as pd

class TechnicalIndicators:

    @staticmethod
    def calculate_daily_returns(data: pd.DataFrame) -> pd.Series:
        """
        Calculate daily percentage returns using closing prices.
        """
        return data["close"].pct_change() * 100

    @staticmethod
    def calculate_sma(
        data: pd.DataFrame,
        window: int
    ) -> pd.Series:
        """
        Calculate Simple Moving Average.
        """
        if window <= 0:
            raise ValueError("Window must be greater than zero")

        return data["close"].rolling(
            window=window,
            min_periods=window
        ).mean()

    @staticmethod
    def calculate_sma_20(data: pd.DataFrame) -> pd.Series:
        return TechnicalIndicators.calculate_sma(
            data=data,
            window=20
        )

    @staticmethod
    def calculate_sma_50(data: pd.DataFrame) -> pd.Series:
        return TechnicalIndicators.calculate_sma(
            data=data,
            window=50
        )
        
    
    @staticmethod
    def calculate_ema(
        data: pd.DataFrame,
        window: int = 20
    ) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        """
        if window <= 0:
            raise ValueError("Window must be greater than zero")

        return data["close"].ewm(
            span=window,
            adjust=False,
            min_periods=window
        ).mean()

    @staticmethod
    def calculate_rsi(
        data: pd.DataFrame,
        window: int = 14
    ) -> pd.Series:
        """
        Calculate Relative Strength Index.
        """
        if window <= 0:
            raise ValueError("Window must be greater than zero")

        delta = data["close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / window,
            adjust=False,
            min_periods=window
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / window,
            adjust=False,
            min_periods=window
        ).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        rsi = rsi.mask(
            (avg_loss == 0) & (avg_gain > 0),
            100.0
        )

        rsi = rsi.mask(
            (avg_gain == 0) & (avg_loss > 0),
            0.0
        )

        rsi = rsi.mask(
            (avg_gain == 0) & (avg_loss == 0),
            50.0
        )

        return rsi

    @staticmethod
    def calculate_macd(
        data: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> pd.DataFrame:
        """
        Calculate MACD, Signal Line and Histogram.
        """
        if fast <= 0 or slow <= 0 or signal <= 0:
            raise ValueError("All MACD windows must be positive")

        if fast >= slow:
            raise ValueError("Fast window must be smaller than slow window")

        fast_ema = data["close"].ewm(
            span=fast,
            adjust=False,
            min_periods=fast
        ).mean()

        slow_ema = data["close"].ewm(
            span=slow,
            adjust=False,
            min_periods=slow
        ).mean()

        macd_line = fast_ema - slow_ema

        signal_line = macd_line.ewm(
            span=signal,
            adjust=False,
            min_periods=signal
        ).mean()

        histogram = macd_line - signal_line

        return pd.DataFrame({
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        })
    
    
    @staticmethod
    def calculate_volatility(
        data: pd.DataFrame,
        window: int = 20,
        annualize: bool = True
    ) -> pd.Series:
        """
        Calculate rolling historical volatility using daily returns.
        """
        if window <= 1:
            raise ValueError("Window must be greater than 1")

        daily_returns = data["close"].pct_change()

        volatility = daily_returns.rolling(
            window=window,
            min_periods=window
        ).std()

        if annualize:
            volatility = volatility * (252 ** 0.5)

        return volatility * 100
    
    
    
    @staticmethod
    def calculate_all_indicators(
        data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate all technical indicators for stock data.
        """

        result = data.copy()

        result["daily_returns"] = (
            TechnicalIndicators.calculate_daily_returns(result)
        )

        result["sma_20"] = (
            TechnicalIndicators.calculate_sma_20(result)
        )

        result["sma_50"] = (
            TechnicalIndicators.calculate_sma_50(result)
        )

        result["ema_20"] = (
            TechnicalIndicators.calculate_ema(result, window=20)
        )

        result["rsi_14"] = (
            TechnicalIndicators.calculate_rsi(result, window=14)
        )

        result["volatility_20"] = (
            TechnicalIndicators.calculate_volatility(
                result,
                window=20
            )
        )

        macd = TechnicalIndicators.calculate_macd(result)

        result = pd.concat(
            [result, macd],
            axis=1
        )

        return result


