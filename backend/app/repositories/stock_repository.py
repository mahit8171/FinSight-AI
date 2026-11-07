from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.schemas.stock import StockCreate , StockUpdate

class StockRepository:
    
    def create(self, db: Session, stock_data: StockCreate):
        new_stock = Stock(**stock_data.model_dump())
        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)
        return new_stock
    
    def get_all(self, db: Session):
        return db.query(Stock).all()
    
    def get_by_id(self, db: Session, stock_id: int):
        return db.query(Stock).filter(Stock.id == stock_id).first()
    
    def get_by_symbol(self, db: Session, symbol: str):
        return db.query(Stock).filter(Stock.symbol == symbol).first()
    
    def update(self, db: Session, stock: Stock, stock_data: StockUpdate):
        
        update_data = stock_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(stock, key, value)
        db.commit()
        db.refresh(stock)
        return stock

    def delete(self, db: Session, stock: Stock):
        db.delete(stock)
        db.commit()
        return True
    
stock_repository = StockRepository()
