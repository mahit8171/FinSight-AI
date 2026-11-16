
from sqlalchemy import (
    Column,
    Integer,
    Float,
    BigInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from app.db.database import Base


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)

    stock_id = Column(
        Integer,
        ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    date = Column(DateTime(timezone=True), nullable=False)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "stock_id",
            "date",
            name="uq_stock_price_stock_date"
        ),
    )
