from datetime import datetime
from pydantic import BaseModel, Field , ConfigDict

#Schema for creating a stock

class StockCreate(BaseModel):
    symbol : str = Field(min_length=1 , max_length=20)
    company_name : str = Field(min_length=1 , max_length=255)
    exchange : str | None = Field(default=None , min_length=1 , max_length=50)
    sector : str | None = Field(default=None , min_length=1 , max_length=100)
    
#Schema for updating a stock

class StockUpdate(BaseModel):
    symbol : str | None = Field(default=None , min_length=1 , max_length=20)
    company_name : str | None = Field(default=None , min_length=1 , max_length=255)
    exchange : str | None = Field(default=None , min_length=1 , max_length=50)
    sector : str | None = Field(default=None , min_length=1 , max_length=100)
    
# Schema for returning stock data 

class StockResponse(BaseModel):
    id : int
    symbol : str
    company_name : str
    exchange : str | None
    sector : str | None
    created_at : datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
