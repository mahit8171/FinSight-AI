from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class WatchlistCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class WatchlistUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)