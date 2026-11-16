from app.db.database import SessionLocal
from app.repositories.stock_repository import stock_repository
from app.repositories.stock_price_repository import stock_price_repository

db = SessionLocal()

try:
    stock = stock_repository.get_by_symbol(
        db=db,
        symbol="RELIANCE"
    )

    if stock:
        total, records = stock_price_repository.get_historical_prices(
            db=db,
            stock_id=stock.id,
            skip=0,
            limit=1000
        )

        print("Stock:", stock.symbol)
        print("Historical records:", total)

finally:
    db.close()