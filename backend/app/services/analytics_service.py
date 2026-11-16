
import pandas as pd

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.stock_repository import stock_repository
from app.repositories.stock_price_repository import (
    stock_price_repository
)
from app.analytics.technical_indicators import TechnicalIndicators


class AnalyticsService:

    def get_stock_analytics(
        self,
        db: Session,
        symbol: str,
        limit: int = 250
    ):

        # 1. Find stock
        stock = stock_repository.get_by_symbol(
            db=db,
            symbol=symbol
        )

        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol} not found"
            )

        # 2. Fetch historical prices
        total_records, records = (
            stock_price_repository.get_historical_prices(
                db=db,
                stock_id=stock.id,
                skip=0,
                limit=limit
            )
        )

        if not records:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for {symbol}"
            )

        # 3. Convert database records into DataFrame
        data = pd.DataFrame([
            {
                "date": record.date,
                "close": record.close
            }
            for record in records
        ])

        # 4. Calculate indicators
        result = TechnicalIndicators.calculate_all_indicators(
            data
        )

        # 5. Replace NaN and infinity for JSON compatibility
        result = result.replace(
            [float("inf"), float("-inf")],
            float("nan")
        )

        result = result.astype(object).where(
            pd.notna(result),
            None
        )

        # 6. Convert DataFrame to dictionary
        analytics_data = result.to_dict(
            orient="records"
        )

        for item in analytics_data:
            if item["date"] is not None:
                item["date"] = item["date"].isoformat()

        return {
            "symbol": stock.symbol,
            "total_records": total_records,
            "returned_records": len(analytics_data),
            "data": analytics_data
        }


analytics_service = AnalyticsService()
