from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.stock_repository import stock_repository
from app.schemas.stock import StockCreate, StockUpdate


class StockService:

    def create_stock(self, db: Session, stock_data: StockCreate):
    
        existing_stock = stock_repository.get_by_symbol(
            db,
            stock_data.symbol
        )

        if existing_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Stock symbol already exists"
            )

        return stock_repository.create(db, stock_data)

    def get_all_stocks(self, db: Session):

        return stock_repository.get_all(db)

    def get_stock(self, db: Session, stock_id: int):

        stock = stock_repository.get_by_id(db, stock_id)

        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )

        return stock

    def update_stock(
        self,
        db: Session,
        stock_id: int,
        stock_data: StockUpdate
    ):

        stock = self.get_stock(db, stock_id)

        update_data = stock_data.model_dump(exclude_unset=True)

        if "symbol" in update_data:
            existing_stock = stock_repository.get_by_symbol(
                db,
                update_data["symbol"]
            )

            if existing_stock and existing_stock.id != stock_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Stock symbol already exists"
                )

        return stock_repository.update(
            db,
            stock,
            stock_data
        )

    def delete_stock(self, db: Session, stock_id: int):

        stock = self.get_stock(db, stock_id)

        stock_repository.delete(db, stock)

        return {"message": "Stock deleted successfully"}


stock_service = StockService()