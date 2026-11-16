
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user

from app.schemas.portfolio_holding import (
    PortfolioHoldingCreate,
    PortfolioHoldingUpdate,
    PortfolioHoldingResponse
)

from app.services.portfolio_holding_service import (
    portfolio_holding_service
)


router = APIRouter(
    prefix="/portfolios/{portfolio_id}/holdings",
    tags=["Portfolio Holdings"]
)


# ADD STOCK HOLDING
@router.post(
    "/",
    response_model=PortfolioHoldingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_holding(
    portfolio_id: int,
    holding_data: PortfolioHoldingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_holding_service.create_holding(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
        holding_data=holding_data
    )


# GET ALL HOLDINGS
@router.get(
    "/",
    response_model=list[PortfolioHoldingResponse]
)
def get_holdings(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_holding_service.get_holdings(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id
    )


# GET SINGLE HOLDING
@router.get(
    "/{holding_id}",
    response_model=PortfolioHoldingResponse
)
def get_holding(
    portfolio_id: int,
    holding_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_holding_service.get_holding(
        db=db,
        portfolio_id=portfolio_id,
        holding_id=holding_id,
        user_id=current_user.id
    )


# UPDATE HOLDING
@router.patch(
    "/{holding_id}",
    response_model=PortfolioHoldingResponse
)
def update_holding(
    portfolio_id: int,
    holding_id: int,
    update_data: PortfolioHoldingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return portfolio_holding_service.update_holding(
        db=db,
        portfolio_id=portfolio_id,
        holding_id=holding_id,
        user_id=current_user.id,
        update_data=update_data
    )


# DELETE HOLDING
@router.delete(
    "/{holding_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_holding(
    portfolio_id: int,
    holding_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    portfolio_holding_service.delete_holding(
        db=db,
        portfolio_id=portfolio_id,
        holding_id=holding_id,
        user_id=current_user.id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
