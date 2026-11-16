from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import dashboard_repository
from app.services.portfolio_analytics_service import (
    portfolio_analytics_service
)

from app.schemas.dashboard import (
    DashboardResponse,
    TopStock
)


def get_dashboard(db: Session, user_id: int):

    # 1. Get user's portfolios
    portfolios = dashboard_repository.get_user_portfolios(
        db=db,
        user_id=user_id
    )

    total_portfolios = len(portfolios)

    # 2. Initialize totals
    total_investment = 0.0
    current_value = 0.0
    all_holdings = []

    # 3. Calculate portfolio analytics
    for portfolio in portfolios:

        analytics = (
            portfolio_analytics_service.get_portfolio_analytics(
                db=db,
                portfolio_id=portfolio.id,
                user_id=user_id
            )
        )

        total_investment += analytics.total_investment
        current_value += analytics.current_value

        all_holdings.extend(analytics.holdings)

    # 4. Calculate total profit/loss
    total_profit_loss = current_value - total_investment

    total_profit_loss_percentage = (
        (total_profit_loss / total_investment) * 100
        if total_investment > 0
        else 0
    )

    # 5. Count unique stocks
    total_stocks = len({
        holding.stock_id for holding in all_holdings
    })

    # 6. Get top performing stocks
    top_performing_stocks = sorted(
        all_holdings,
        key=lambda holding: holding.profit_loss_percentage,
        reverse=True
    )[:5]

    top_stocks = [
        TopStock(
            stock_id=holding.stock_id,
            symbol=holding.symbol,
            current_value=holding.current_value,
            profit_loss=holding.profit_loss,
            profit_loss_percentage=holding.profit_loss_percentage
        )
        for holding in top_performing_stocks
    ]

    # 7. Return dashboard response
    return DashboardResponse(
        total_portfolios=total_portfolios,
        total_investment=round(total_investment, 2),
        current_value=round(current_value, 2),
        total_profit_loss=round(total_profit_loss, 2),
        total_profit_loss_percentage=round(
            total_profit_loss_percentage, 2
        ),
        total_stocks=total_stocks,
        top_performing_stocks=top_stocks
    )   