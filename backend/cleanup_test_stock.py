from app.db.database import SessionLocal
from app.models.stock import Stock

db = SessionLocal()

try:
    stock = db.query(Stock).filter(
        Stock.symbol == "TESTSHORT"
    ).first()

    if stock:
        db.delete(stock)
        db.commit()
        print("TESTSHORT deleted successfully")
    else:
        print("TESTSHORT not found")

finally:
    db.close()