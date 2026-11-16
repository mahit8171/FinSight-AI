
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.portfolio_repository import portfolio_repository
from app.repositories.portfolio_holding_repository import (
    portfolio_holding_repository
)
from app.repositories.stock_repository import stock_repository
from app.repositories.stock_price_repository import (
    stock_price_repository
)

from app.schemas.portfolio_analytics import (
    HoldingAnalytics,
    PortfolioAnalyticsResponse
)


class PortfolioAnalyticsService:

    def get_portfolio_analytics(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ):

        # 1. Verify portfolio ownership
        portfolio = portfolio_repository.get_by_id(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )

        # 2. Fetch all holdings
        holdings = portfolio_holding_repository.get_all_by_portfolio(
            db=db,
            portfolio_id=portfolio_id
        )

        total_investment = 0.0
        current_value = 0.0

        holding_analytics = []

        # 3. Calculate individual stock analytics
        for holding in holdings:

            stock = stock_repository.get_by_id(
                db=db,
                stock_id=holding.stock_id
            )

            if not stock:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Stock not found: {holding.stock_id}"
                )

            latest_price = stock_price_repository.get_latest_price(
                db=db,
                stock_id=holding.stock_id
            )

            if latest_price is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Price history unavailable for {stock.symbol}"
                )

            # Investment calculation
            invested_value = (
                holding.quantity * holding.average_buy_price
            )

            # Current market value based on latest closing price
            current_stock_price = latest_price.close

            stock_current_value = (
                holding.quantity * current_stock_price
            )

            # Profit / Loss
            profit_loss = (
                stock_current_value - invested_value
            )

            if invested_value > 0:
                profit_loss_percentage = (
                    profit_loss / invested_value
                ) * 100
            else:
                profit_loss_percentage = 0.0

            total_investment += invested_value
            current_value += stock_current_value

            holding_analytics.append({
                "stock_id": stock.id,
                "symbol": stock.symbol,
                "quantity": holding.quantity,
                "average_buy_price": holding.average_buy_price,
                "invested_value": round(invested_value, 2),
                "current_price": round(current_stock_price, 2),
                "current_value": round(stock_current_value, 2),
                "profit_loss": round(profit_loss, 2),
                "profit_loss_percentage": round(
                    profit_loss_percentage, 2
                ),
                "allocation_percentage": 0.0
            })

        # 4. Total portfolio profit/loss
        total_profit_loss = current_value - total_investment

        if total_investment > 0:
            total_profit_loss_percentage = (
                total_profit_loss / total_investment
            ) * 100
        else:
            total_profit_loss_percentage = 0.0

        # 5. Calculate stock allocation
        for item in holding_analytics:
            if current_value > 0:
                item["allocation_percentage"] = round(
                    (item["current_value"] / current_value) * 100,
                    2
                )

        # 6. Final response
        return PortfolioAnalyticsResponse(
            portfolio_id=portfolio.id,
            portfolio_name=portfolio.name,
            total_investment=round(total_investment, 2),
            current_value=round(current_value, 2),
            total_profit_loss=round(total_profit_loss, 2),
            total_profit_loss_percentage=round(
                total_profit_loss_percentage, 2
            ),
            holdings=holding_analytics
        )


portfolio_analytics_service = PortfolioAnalyticsService()
