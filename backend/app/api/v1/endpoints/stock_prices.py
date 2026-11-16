
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.stock_price_service import stock_price_service
from app.schemas.stock_price import (
    StockPriceResponse,
    StockHistoryResponse
)


router = APIRouter(
    prefix="/stocks",
    tags=["Stock Price History"]
)


# ==========================================
# 1. Historical Stock Prices
# ==========================================

@router.get(
    "/{symbol}/history",
    response_model=StockHistoryResponse
)
def get_stock_history(
    symbol: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return stock_price_service.get_historical_prices(
        db=db,
        symbol=symbol.upper(),
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )


# ==========================================
# 2. Latest Stock Price
# ==========================================

@router.get(
    "/{symbol}/history/latest"
)
def get_latest_stock_price(
    symbol: str,
    db: Session = Depends(get_db)
):
    result = stock_price_service.get_latest_price(
        db=db,
        symbol=symbol.upper()
    )

    return {
        "symbol": result["symbol"],
        "data": StockPriceResponse.model_validate(
            result["data"]
        )
    }
