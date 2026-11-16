from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.portfolio_holding import PortfolioHolding


def get_total_portfolios(db: Session, user_id: int):
    return (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id)
        .count()
    )


def get_user_portfolios(db: Session, user_id: int):
    return (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id)
        .all()
    )


def get_total_holdings(db: Session, user_id: int):
    return (
        db.query(PortfolioHolding)
        .join(
            Portfolio,
            Portfolio.id == PortfolioHolding.portfolio_id
        )
        .filter(Portfolio.user_id == user_id)
        .count()
    )