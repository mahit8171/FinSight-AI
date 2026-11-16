from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class WatchlistItemCreate(BaseModel):
    stock_id: int = Field(gt=0)


class WatchlistItemResponse(BaseModel):
    id: int
    watchlist_id: int
    stock_id: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)