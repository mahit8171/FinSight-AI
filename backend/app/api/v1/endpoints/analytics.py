
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.analytics_service import analytics_service


router = APIRouter(
    prefix="/stocks",
    tags=["Stock Analytics"]
)


@router.get("/{symbol}/analytics")
def get_stock_analytics(
    symbol: str,
    limit: int = Query(default=250, ge=50, le=1000),
    db: Session = Depends(get_db)
):
    return analytics_service.get_stock_analytics(
        db=db,
        symbol=symbol.upper(),
        limit=limit
    )
