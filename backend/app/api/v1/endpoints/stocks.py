from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.stock import (
    StockCreate,
    StockUpdate,
    StockResponse
)
from app.services.stock_service import stock_service

from app.api.deps import get_current_user, get_current_admin
from app.models.user import User


router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)




# CREATE STOCK
@router.post(
    "/",
    response_model=StockResponse,
    status_code=status.HTTP_201_CREATED
)
def create_stock(
    stock_data: StockCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    return stock_service.create_stock(db, stock_data)


# GET ALL STOCKS
@router.get(
    "/",
    response_model=list[StockResponse]
)
def get_all_stocks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return stock_service.get_all_stocks(db)


# GET STOCK BY ID
@router.get(
    "/{stock_id}",
    response_model=StockResponse
)
def get_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return stock_service.get_stock(db, stock_id)


# UPDATE STOCK
@router.patch(
    "/{stock_id}",
    response_model=StockResponse
)
def update_stock(
    stock_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    return stock_service.update_stock(
        db,
        stock_id,
        stock_data
    )


# DELETE STOCK
@router.delete(
    "/{stock_id}"
)
def delete_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    return stock_service.delete_stock(db, stock_id)