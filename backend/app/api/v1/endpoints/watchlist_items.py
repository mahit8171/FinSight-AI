from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user

from app.schemas.watchlist_item import (
    WatchlistItemCreate,
    WatchlistItemResponse
)

from app.services import watchlist_service


router = APIRouter(
    prefix="/watchlists/{watchlist_id}/items",
    tags=["Watchlist Items"]
)


@router.post(
    "/",
    response_model=WatchlistItemResponse,
    status_code=status.HTTP_201_CREATED
)
def add_stock(
    watchlist_id: int,
    payload: WatchlistItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.add_stock(
        db=db,
        watchlist_id=watchlist_id,
        user_id=current_user.id,
        stock_id=payload.stock_id
    )


@router.get("/", response_model=list[WatchlistItemResponse])
def get_stocks(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.get_watchlist_stocks(
        db=db,
        watchlist_id=watchlist_id,
        user_id=current_user.id
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_stock(
    watchlist_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    watchlist_service.remove_stock(
        db=db,
        watchlist_id=watchlist_id,
        item_id=item_id,
        user_id=current_user.id
    )