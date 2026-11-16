
from datetime import datetime, timedelta, timezone

from app.db.database import SessionLocal
from app.models.stock import Stock
from app.models.stock_price import StockPrice


db = SessionLocal()

try:
    # Check whether test stock already exists
    stock = db.query(Stock).filter(
        Stock.symbol == "TESTSHORT"
    ).first()

    if stock is None:
        stock = Stock(
            symbol="TESTSHORT",
            company_name="Test Short History",
            exchange="TEST",
            sector="Testing"
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)

    # Check existing test records
    existing_count = db.query(StockPrice).filter(
        StockPrice.stock_id == stock.id
    ).count()

    if existing_count == 0:
        base_date = datetime(2026, 1, 1, tzinfo=timezone.utc)

        for i in range(10):
            close_price = 100 + (i * 2)

            record = StockPrice(
                stock_id=stock.id,
                date=base_date + timedelta(days=i),
                open=close_price - 1,
                high=close_price + 2,
                low=close_price - 2,
                close=close_price,
                volume=100000
            )

            db.add(record)

        db.commit()

    print("Test stock:", stock.symbol)

    final_count = db.query(StockPrice).filter(
        StockPrice.stock_id == stock.id
    ).count()

    print("Historical records:", final_count)

finally:
    db.close()
