
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# Create Portfolio
class PortfolioCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None


# Update Portfolio
class PortfolioUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: str | None = None


# Portfolio Response
class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
