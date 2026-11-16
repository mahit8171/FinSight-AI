
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StockPriceResponse(BaseModel):

    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    model_config = ConfigDict(from_attributes=True)


class StockHistoryResponse(BaseModel):

    symbol: str
    total_records: int
    data: list[StockPriceResponse]

