from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user

from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistUpdate,
    WatchlistResponse
)

from app.services import watchlist_service


router = APIRouter(
    prefix="/watchlists",
    tags=["Watchlists"]
)


@router.post(
    "/",
    response_model=WatchlistResponse,
    status_code=status.HTTP_201_CREATED
)
def create_watchlist(
    payload: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.create_watchlist(
        db=db,
        user_id=current_user.id,
        name=payload.name
    )


@router.get("/", response_model=list[WatchlistResponse])
def get_watchlists(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.get_all_watchlists(
        db=db,
        user_id=current_user.id
    )


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
def get_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.get_watchlist(
        db=db,
        watchlist_id=watchlist_id,
        user_id=current_user.id
    )


@router.patch("/{watchlist_id}", response_model=WatchlistResponse)
def update_watchlist(
    watchlist_id: int,
    payload: WatchlistUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return watchlist_service.update_watchlist(
        db=db,
        watchlist_id=watchlist_id,
        user_id=current_user.id,
        name=payload.name
    )


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    watchlist_service.delete_watchlist(
        db=db,
        watchlist_id=watchlist_id,
        user_id=current_user.id
    )