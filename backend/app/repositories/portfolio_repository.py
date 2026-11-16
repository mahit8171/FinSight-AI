
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


class PortfolioRepository:

    def create(
        self,
        db: Session,
        user_id: int,
        name: str,
        description: str | None = None
    ):
        portfolio = Portfolio(
            user_id=user_id,
            name=name,
            description=description
        )

        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

        return portfolio

    def get_by_id(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ):
        return (
            db.query(Portfolio)
            .filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            )
            .first()
        )

    def get_all_by_user(
        self,
        db: Session,
        user_id: int
    ):
        return (
            db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .order_by(Portfolio.created_at.desc())
            .all()
        )

    def update(
        self,
        db: Session,
        portfolio: Portfolio,
        update_data: dict
    ):
        for key, value in update_data.items():
            setattr(portfolio, key, value)

        db.commit()
        db.refresh(portfolio)

        return portfolio

    def delete(
        self,
        db: Session,
        portfolio: Portfolio
    ):
        db.delete(portfolio)
        db.commit()


portfolio_repository = PortfolioRepository()
