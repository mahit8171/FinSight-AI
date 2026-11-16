from sqlalchemy.orm import Session

from app.repositories import market_overview_repository
from app.schemas.market_overview import (
    MarketStock,
    MarketOverviewResponse
)


def get_market_overview(db: Session):

    # 1. Get total tracked stocks
    total_stocks = market_overview_repository.get_total_stocks(db)

    # 2. Get latest and previous prices
    market_data = market_overview_repository.get_market_stocks(db)

    stocks = []

    # 3. Calculate price changes
    for item in market_data:

        current_price = item["current_price"]
        previous_price = item["previous_price"]

        change = current_price - previous_price

        change_percentage = (
            (change / previous_price) * 100
            if previous_price > 0
            else 0
        )

        stocks.append(
            MarketStock(
                stock_id=item["stock_id"],
                symbol=item["symbol"],
                company_name=item["company_name"],
                current_price=round(current_price, 2),
                previous_price=round(previous_price, 2),
                change=round(change, 2),
                change_percentage=round(change_percentage, 2)
            )
        )

    # 4. Top gainers
    top_gainers = sorted(
        [stock for stock in stocks if stock.change > 0],
        key=lambda stock: stock.change_percentage,
        reverse=True
    )[:5]

    # 5. Top losers
    top_losers = sorted(
        [stock for stock in stocks if stock.change < 0],
        key=lambda stock: stock.change_percentage
    )[:5]

    # 6. Return response
    return MarketOverviewResponse(
        total_tracked_stocks=total_stocks,
        top_gainers=top_gainers,
        top_losers=top_losers
    )