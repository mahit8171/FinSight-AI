from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import user_repository


class UserService:

    # CREATE USER
    def create_user(self, db: Session, user_data: UserCreate):

        existing_user = user_repository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        hashed_password = hash_password(user_data.password)

        return user_repository.create(
            db,
            user_data,
            hashed_password
        )

    # GET ALL USERS
    def get_all_users(self, db: Session):

        return user_repository.get_all(db)

    # GET USER BY ID
    def get_user(self, db: Session, user_id: int):

        user = user_repository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    # UPDATE USER
    def update_user(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ):

        user = self.get_user(db, user_id)

        update_data = user_data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:
            existing_user = user_repository.get_by_email(
                db,
                update_data["email"]
            )

            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(
                update_data.pop("password")
            )

        return user_repository.update(
            db,
            user,
            update_data
        )

    # DELETE USER
    def delete_user(self, db: Session, user_id: int):

        user = self.get_user(db, user_id)

        user_repository.delete(db, user)

        return {"message": "User deleted successfully"}
    
    
    def login_user(self, db, email: str, password: str):
        user = user_repository.get_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


user_service = UserService()