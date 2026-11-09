from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.services.user_service import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# CREATE USER
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    return user_service.create_user(db, user_data)


# GET ALL USERS
@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db)
):

    return user_service.get_all_users(db)


# GET USER BY ID
@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return user_service.get_user(db, user_id)


# UPDATE USER
@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    return user_service.update_user(
        db,
        user_id,
        user_data
    )


# DELETE USER
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return user_service.delete_user(db, user_id)