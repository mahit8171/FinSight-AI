from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist


def create(db: Session, user_id: int, name: str):
    watchlist = Watchlist(
        user_id=user_id,
        name=name
    )

    db.add(watchlist)
    db.commit()
    db.refresh(watchlist)

    return watchlist


def get_by_id(db: Session, watchlist_id: int, user_id: int):
    return (
        db.query(Watchlist)
        .filter(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == user_id
        )
        .first()
    )


def get_all_by_user(db: Session, user_id: int):
    return (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id)
        .order_by(Watchlist.id.desc())
        .all()
    )


def update(db: Session, watchlist: Watchlist, name: str):
    watchlist.name = name

    db.commit()
    db.refresh(watchlist)

    return watchlist


def delete(db: Session, watchlist: Watchlist):
    db.delete(watchlist)
    db.commit()