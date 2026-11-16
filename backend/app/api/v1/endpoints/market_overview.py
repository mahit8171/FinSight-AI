from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.market_overview import MarketOverviewResponse
from app.services import market_overview_service


router = APIRouter(
    prefix="/market",
    tags=["Market Overview"]
)


@router.get("/overview", response_model=MarketOverviewResponse)
def get_market_overview(
    db: Session = Depends(get_db)
):
    return market_overview_service.get_market_overview(
        db=db
    )