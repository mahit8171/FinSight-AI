
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# CREATE PORTFOLIO HOLDING
class PortfolioHoldingCreate(BaseModel):

    stock_id: int = Field(gt=0)

    quantity: float = Field(gt=0)

    average_buy_price: float = Field(gt=0)


# UPDATE PORTFOLIO HOLDING
class PortfolioHoldingUpdate(BaseModel):

    quantity: float | None = Field(
        default=None,
        gt=0
    )

    average_buy_price: float | None = Field(
        default=None,
        gt=0
    )


# PORTFOLIO HOLDING RESPONSE
class PortfolioHoldingResponse(BaseModel):

    id: int

    portfolio_id: int

    stock_id: int

    quantity: float

    average_buy_price: float

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
