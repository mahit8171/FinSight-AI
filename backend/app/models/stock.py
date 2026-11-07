from sqlalchemy import String , DateTime, null
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.sql import func

from app.db.database import Base

class Stock(Base):
    __tablename__ = "stocks"
    id:Mapped[int] = mapped_column(primary_key=True , index= True)
    
    symbol:Mapped[str] = mapped_column(
        String(20) , 
        unique=True,
        index=True , 
        nullable= False
    )
    
    company_name:Mapped[str] = mapped_column(String(255) , nullable=False)
    
    exchange:Mapped[str] = mapped_column(
        String(50) , 
        nullable= True
    )
    
    sector:Mapped[str] = mapped_column(
        String(100) , 
        nullable= True
    )
    
    created_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone=True) ,
        server_default=func.now()
    )