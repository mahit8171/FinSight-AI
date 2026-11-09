from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import user_service

from app.api.deps import get_current_user
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return user_service.login_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )
    
    
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user