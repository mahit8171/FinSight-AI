
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.portfolio_repository import portfolio_repository
from app.repositories.portfolio_holding_repository import (
    portfolio_holding_repository
)
from app.repositories.stock_repository import stock_repository


class PortfolioHoldingService:

    # CREATE HOLDING
    def create_holding(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int,
        holding_data
    ):
        # Verify portfolio ownership
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

        # Verify stock exists
        stock = stock_repository.get_by_id(
            db=db,
            stock_id=holding_data.stock_id
        )

        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )

        # Prevent duplicate stock holding
        existing_holdings = portfolio_holding_repository.get_all_by_portfolio(
            db=db,
            portfolio_id=portfolio_id
        )

        for holding in existing_holdings:
            if holding.stock_id == holding_data.stock_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Stock already exists in this portfolio"
                )

        return portfolio_holding_repository.create(
            db=db,
            portfolio_id=portfolio_id,
            stock_id=holding_data.stock_id,
            quantity=holding_data.quantity,
            average_buy_price=holding_data.average_buy_price
        )

    # GET ALL HOLDINGS
    def get_holdings(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ):
        portfolio_repository.get_by_id(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        ) or self._portfolio_not_found()

        return portfolio_holding_repository.get_all_by_portfolio(
            db=db,
            portfolio_id=portfolio_id
        )

    # GET SINGLE HOLDING
    def get_holding(
        self,
        db: Session,
        portfolio_id: int,
        holding_id: int,
        user_id: int
    ):
        portfolio = portfolio_repository.get_by_id(
            db=db,
            portfolio_id=portfolio_id,
            user_id=user_id
        )

        if not portfolio:
            self._portfolio_not_found()

        holding = portfolio_holding_repository.get_by_id(
            db=db,
            holding_id=holding_id,
            portfolio_id=portfolio_id
        )

        if not holding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Holding not found"
            )

        return holding

    # UPDATE HOLDING
    def update_holding(
        self,
        db: Session,
        portfolio_id: int,
        holding_id: int,
        user_id: int,
        update_data
    ):
        holding = self.get_holding(
            db=db,
            portfolio_id=portfolio_id,
            holding_id=holding_id,
            user_id=user_id
        )

        data = update_data.model_dump(exclude_unset=True)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        if any(value is None for value in data.values()):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Update values cannot be null"
            )

        return portfolio_holding_repository.update(
            db=db,
            holding=holding,
            update_data=data
        )

    # DELETE HOLDING
    def delete_holding(
        self,
        db: Session,
        portfolio_id: int,
        holding_id: int,
        user_id: int
    ):
        holding = self.get_holding(
            db=db,
            portfolio_id=portfolio_id,
            holding_id=holding_id,
            user_id=user_id
        )

        portfolio_holding_repository.delete(
            db=db,
            holding=holding
        )

    # COMMON ERROR
    def _portfolio_not_found(self):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )


portfolio_holding_service = PortfolioHoldingService()
