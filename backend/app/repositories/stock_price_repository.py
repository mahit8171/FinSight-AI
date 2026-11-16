
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.stock_price import StockPrice
from sqlalchemy import func


class StockPriceRepository:

    def bulk_create(
        self,
        db: Session,
        stock_id: int,
        data: pd.DataFrame
    ):
        records = []

        for _, row in data.iterrows():
            records.append({
                "stock_id": stock_id,
                "date": row["Date"].to_pydatetime(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })

        if not records:
            return 0

        statement = (
            insert(StockPrice)
            .values(records)
            .on_conflict_do_nothing(
                constraint="uq_stock_price_stock_date"
            )
            .returning(StockPrice.id)
        )

        try:
            result = db.execute(statement)
            inserted_count = len(result.fetchall())
            db.commit()
            return inserted_count

        except Exception:
            db.rollback()
            raise
        
    


    def get_latest_date(self, db: Session, stock_id: int):
        return (
            db.query(func.max(StockPrice.date))
            .filter(StockPrice.stock_id == stock_id)
            .scalar()
        )
        
        
    
    def get_historical_prices(
        self,
        db: Session,
        stock_id: int,
        start_date=None,
        end_date=None,
        skip: int = 0,
        limit: int = 100
    ):
        query = (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == stock_id)
        )

        if start_date is not None:
            query = query.filter(
                StockPrice.date >= start_date
            )

        if end_date is not None:
            query = query.filter(
                StockPrice.date <= end_date
            )

        total_records = query.count()

        records = (
            query
            .order_by(StockPrice.date.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return total_records, records

    def get_latest_price(
        self,
        db: Session,
        stock_id: int
    ):
        return (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == stock_id)
            .order_by(StockPrice.date.desc())
            .first()
        )




stock_price_repository = StockPriceRepository()
