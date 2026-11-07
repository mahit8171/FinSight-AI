from datetime import datetime
from pydantic import BaseModel, Field , ConfigDict

#Schema for creating a stock

class StockCreate(BaseModel):
    symbol : str = Field(min_length=1 , max_length=20)
    