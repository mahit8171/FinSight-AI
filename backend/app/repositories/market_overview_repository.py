from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.stock import Stock
from app.models.stock_price import StockPrice


def get_total_stocks(db: Session):
    return db.query(Stock).count()


def get_market_stocks(db: Session):
    stocks = db.query(Stock).all()

    market_data = []

    for stock in stocks:

        prices = (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == stock.id)
            .order_by(desc(StockPrice.date))
            .limit(2)
            .all()
        )

        if len(prices) < 2:
            continue

        market_data.append({
            "stock_id": stock.id,
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "current_price": prices[0].close,
            "previous_price": prices[1].close
        })

    return market_data