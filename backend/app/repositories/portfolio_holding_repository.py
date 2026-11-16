
from sqlalchemy.orm import Session

from app.models.portfolio_holding import PortfolioHolding


class PortfolioHoldingRepository:

    # CREATE HOLDING
    def create(
        self,
        db: Session,
        portfolio_id: int,
        stock_id: int,
        quantity: float,
        average_buy_price: float
    ):
        holding = PortfolioHolding(
            portfolio_id=portfolio_id,
            stock_id=stock_id,
            quantity=quantity,
            average_buy_price=average_buy_price
        )

        db.add(holding)
        db.commit()
        db.refresh(holding)

        return holding

    # GET HOLDING BY ID
    def get_by_id(
        self,
        db: Session,
        holding_id: int,
        portfolio_id: int
    ):
        return (
            db.query(PortfolioHolding)
            .filter(
                PortfolioHolding.id == holding_id,
                PortfolioHolding.portfolio_id == portfolio_id
            )
            .first()
        )

    # GET ALL HOLDINGS OF PORTFOLIO
    def get_all_by_portfolio(
        self,
        db: Session,
        portfolio_id: int
    ):
        return (
            db.query(PortfolioHolding)
            .filter(
                PortfolioHolding.portfolio_id == portfolio_id
            )
            .order_by(PortfolioHolding.id.asc())
            .all()
        )

    # UPDATE HOLDING
    def update(
        self,
        db: Session,
        holding: PortfolioHolding,
        update_data: dict
    ):
        for key, value in update_data.items():
            setattr(holding, key, value)

        db.commit()
        db.refresh(holding)

        return holding

    # DELETE HOLDING
    def delete(
        self,
        db: Session,
        holding: PortfolioHolding
    ):
        db.delete(holding)
        db.commit()


portfolio_holding_repository = PortfolioHoldingRepository()
