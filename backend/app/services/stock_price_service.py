
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.repositories.stock_repository import stock_repository
from app.repositories.stock_price_repository import stock_price_repository


class StockPriceService:

    def save_stock_prices(
        self,
        db: Session,
        symbol: str,
        data
    ):
        # Check whether stock exists
        stock = stock_repository.get_by_symbol(db, symbol)

        if stock is None:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol} not found"
            )

        # Save historical prices
        total_records = stock_price_repository.bulk_create(
            db=db,
            stock_id=stock.id,
            data=data
        )

        return {
            "message": "Stock prices saved successfully",
            "symbol": symbol,
            "stock_id": stock.id,
            "total_records": total_records
        }
        
    


    def get_next_fetch_date(self, db: Session, stock_id: int):
        latest_date = stock_price_repository.get_latest_date(
            db=db,
            stock_id=stock_id
        )

        if latest_date is None:
            return None

        return latest_date.date() + timedelta(days=1)
    
    
    def get_historical_prices(
        self,
        db: Session,
        symbol: str,
        start_date=None,
        end_date=None,
        skip: int = 0,
        limit: int = 100
    ):
        # Find stock by symbol
        stock = stock_repository.get_by_symbol(db, symbol)

        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol} not found"
            )

        # Fetch historical prices
        total_records, records = (
            stock_price_repository.get_historical_prices(
                db=db,
                stock_id=stock.id,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit
            )
        )

        return {
            "symbol": stock.symbol,
            "total_records": total_records,
            "data": records
        }

    def get_latest_price(
        self,
        db: Session,
        symbol: str
    ):
        # Find stock
        stock = stock_repository.get_by_symbol(db, symbol)

        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol} not found"
            )

        # Fetch latest price
        latest_price = stock_price_repository.get_latest_price(
            db=db,
            stock_id=stock.id
        )

        if not latest_price:
            raise HTTPException(
                status_code=404,
                detail=f"No price history found for {symbol}"
            )

        return {
            "symbol": stock.symbol,
            "data": latest_price
        }




stock_price_service = StockPriceService()
