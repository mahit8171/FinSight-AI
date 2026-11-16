
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.portfolio_repository import portfolio_repository


class PortfolioService:

    def create_portfolio(
        self,
        db: Session,
        user_id: int,
        portfolio_data
    ):
        return portfolio_repository.create(
            db=db,
            user_id=user_id,
            name=portfolio_data.name,
            description=portfolio_data.description
        )

    def get_portfolios(
        self,
        db: Session,
        user_id: int
    ):
        return portfolio_repository.get_all_by_user(
            db=db,
            user_id=user_id
        )

    def get_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ):
        portfolio = portfolio_repository.get_by_id(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found"
            )

        return portfolio

    def update_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
        update_data
    ):
        portfolio = self.get_portfolio(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        )

        data = update_data.model_dump(exclude_unset=True)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        return portfolio_repository.update(
            db=db,
            portfolio=portfolio,
            update_data=data
        )

    def delete_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ):
        portfolio = self.get_portfolio(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        )

        portfolio_repository.delete(
            db=db,
            portfolio=portfolio
        )


portfolio_service = PortfolioService()
