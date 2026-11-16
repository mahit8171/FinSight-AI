from pydantic import BaseModel
from typing import List


class TopStock(BaseModel):
    stock_id: int
    symbol: str
    current_value: float
    profit_loss: float
    profit_loss_percentage: float


class DashboardResponse(BaseModel):
    total_portfolios: int
    total_investment: float
    current_value: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    total_stocks: int
    top_performing_stocks: List[TopStock]