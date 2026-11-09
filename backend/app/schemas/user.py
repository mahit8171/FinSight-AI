from datetime import datetime
from pydantic import BaseModel, Field , ConfigDict , EmailStr

# USER Registration

class UserCreate(BaseModel):
    name : str = Field(min_length=1 , max_length=100)
    email : EmailStr
    password : str = Field(min_length=8 , max_length=128)
    
    
# USER Update
class UserUpdate(BaseModel):
    name : str | None = Field(default=None , min_length=1 , max_length=100)
    email : EmailStr | None = None
    password : str | None = Field(default=None , min_length=8 , max_length=128)
    is_active : bool | None = Field(default=None)
    
# User API Response
class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    is_active : bool
    created_at : datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )