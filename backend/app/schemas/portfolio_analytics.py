
from pydantic import BaseModel
from typing import List


class HoldingAnalytics(BaseModel):
    stock_id: int
    symbol: str

    quantity: float
    average_buy_price: float

    invested_value: float
    current_price: float
    current_value: float

    profit_loss: float
    profit_loss_percentage: float

    allocation_percentage: float


class PortfolioAnalyticsResponse(BaseModel):
    portfolio_id: int
    portfolio_name: str

    total_investment: float
    current_value: float

    total_profit_loss: float
    total_profit_loss_percentage: float

    holdings: List[HoldingAnalytics]
