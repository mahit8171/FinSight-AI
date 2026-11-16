
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse
)
from app.services.portfolio_service import portfolio_service


router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"]
)


@router.post(
    "/",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED
)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_service.create_portfolio(
        db=db,
        user_id=current_user.id,
        portfolio_data=portfolio_data
    )


@router.get(
    "/",
    response_model=list[PortfolioResponse]
)
def get_portfolios(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_service.get_portfolios(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_service.get_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id
    )


@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioResponse
)
def update_portfolio(
    portfolio_id: int,
    update_data: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_service.update_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
        update_data=update_data
    )


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    portfolio_service.delete_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
