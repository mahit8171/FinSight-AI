
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user

from app.schemas.portfolio_analytics import (
    PortfolioAnalyticsResponse
)

from app.services.portfolio_analytics_service import (
    portfolio_analytics_service
)


router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolio Analytics"]
)


@router.get(
    "/{portfolio_id}/analytics",
    response_model=PortfolioAnalyticsResponse
)
def get_portfolio_analytics(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_analytics_service.get_portfolio_analytics(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id
    )
