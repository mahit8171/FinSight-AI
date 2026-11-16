from pydantic import BaseModel
from typing import List


class MarketStock(BaseModel):
    stock_id: int
    symbol: str
    company_name: str
    current_price: float
    previous_price: float
    change: float
    change_percentage: float


class MarketOverviewResponse(BaseModel):
    total_tracked_stocks: int
    top_gainers: List[MarketStock]
    top_losers: List[MarketStock]