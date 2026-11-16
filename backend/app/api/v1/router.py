
from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    stocks,
    users,
    auth,
    stock_prices,
    analytics,
    portfolios,
    portfolio_holdings,
    portfolio_analytics,
    watchlists,
    watchlist_items,
    dashboard,
    market_overview,
    stock_search,
    predictions,
    ml_predictions,  
)


api_router = APIRouter()


api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    stocks.router
)

api_router.include_router(
    users.router
)

api_router.include_router(
    auth.router
)

api_router.include_router(
    stock_prices.router
)

api_router.include_router(
    analytics.router
)


api_router.include_router(
    portfolios.router
)

api_router.include_router(
    portfolio_holdings.router
)

api_router.include_router(
    portfolio_analytics.router
)

api_router.include_router(watchlists.router)

api_router.include_router(watchlist_items.router)

api_router.include_router(dashboard.router)

api_router.include_router(market_overview.router)

api_router.include_router(
    stock_search.router,
    prefix="/stocks/search",
    tags=["Stock Search"]
)


api_router.include_router(
    predictions.router
)


api_router.include_router(
    ml_predictions.router
)