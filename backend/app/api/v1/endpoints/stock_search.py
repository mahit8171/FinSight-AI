
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.stock_search_service import stock_search_service
from app.schemas.stock import StockResponse

router = APIRouter()


@router.get("/", response_model=list[StockResponse])
def search_stocks(
    q: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return stock_search_service.search_stocks(
        db=db,
        query=q,
        limit=limit
    )
