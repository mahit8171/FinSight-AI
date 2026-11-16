from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import watchlist_repository
from app.repositories import watchlist_item_repository
from app.repositories.stock_repository import stock_repository


def create_watchlist(db: Session, user_id: int, name: str):
    return watchlist_repository.create(
        db=db,
        user_id=user_id,
        name=name
    )


def get_all_watchlists(db: Session, user_id: int):
    return watchlist_repository.get_all_by_user(
        db=db,
        user_id=user_id
    )


def get_watchlist(db: Session, watchlist_id: int, user_id: int):
    watchlist = watchlist_repository.get_by_id(
        db=db,
        watchlist_id=watchlist_id,
        user_id=user_id
    )

    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )

    return watchlist


def update_watchlist(
    db: Session,
    watchlist_id: int,
    user_id: int,
    name: str
):
    watchlist = get_watchlist(db, watchlist_id, user_id)

    return watchlist_repository.update(
        db=db,
        watchlist=watchlist,
        name=name
    )


def delete_watchlist(
    db: Session,
    watchlist_id: int,
    user_id: int
):
    watchlist = get_watchlist(db, watchlist_id, user_id)

    watchlist_repository.delete(db, watchlist)

    return {"message": "Watchlist deleted successfully"}


def add_stock(
    db: Session,
    watchlist_id: int,
    user_id: int,
    stock_id: int
):
    # Verify watchlist ownership
    get_watchlist(db, watchlist_id, user_id)

    # Verify stock exists
    stock = stock_repository.get_by_id(db, stock_id)

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )

    # Prevent duplicate stock
    existing_item = watchlist_item_repository.get_by_stock(
        db=db,
        watchlist_id=watchlist_id,
        stock_id=stock_id
    )

    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Stock already exists in this watchlist"
        )

    return watchlist_item_repository.create(
        db=db,
        watchlist_id=watchlist_id,
        stock_id=stock_id
    )


def get_watchlist_stocks(
    db: Session,
    watchlist_id: int,
    user_id: int
):
    get_watchlist(db, watchlist_id, user_id)

    return watchlist_item_repository.get_all_by_watchlist(
        db=db,
        watchlist_id=watchlist_id
    )


def remove_stock(
    db: Session,
    watchlist_id: int,
    item_id: int,
    user_id: int
):
    get_watchlist(db, watchlist_id, user_id)

    item = watchlist_item_repository.get_by_id(
        db=db,
        item_id=item_id,
        watchlist_id=watchlist_id
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )

    watchlist_item_repository.delete(db, item)

    return {"message": "Stock removed from watchlist successfully"}