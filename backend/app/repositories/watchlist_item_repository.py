from sqlalchemy.orm import Session

from app.models.watchlist_item import WatchlistItem


def create(db: Session, watchlist_id: int, stock_id: int):
    item = WatchlistItem(
        watchlist_id=watchlist_id,
        stock_id=stock_id
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_by_id(
    db: Session,
    item_id: int,
    watchlist_id: int
):
    return (
        db.query(WatchlistItem)
        .filter(
            WatchlistItem.id == item_id,
            WatchlistItem.watchlist_id == watchlist_id
        )
        .first()
    )


def get_all_by_watchlist(db: Session, watchlist_id: int):
    return (
        db.query(WatchlistItem)
        .filter(WatchlistItem.watchlist_id == watchlist_id)
        .order_by(WatchlistItem.id.desc())
        .all()
    )


def get_by_stock(db: Session, watchlist_id: int, stock_id: int):
    return (
        db.query(WatchlistItem)
        .filter(
            WatchlistItem.watchlist_id == watchlist_id,
            WatchlistItem.stock_id == stock_id
        )
        .first()
    )


def delete(db: Session, item: WatchlistItem):
    db.delete(item)
    db.commit()