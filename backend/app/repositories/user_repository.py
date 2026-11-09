from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:

    def create(
    self,
    db: Session,
    user_data: UserCreate,
    hashed_password: str
    ):

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def get_all(self, db: Session):

        return db.query(User).all()

    def get_by_id(self, db: Session, user_id: int):

        return db.query(User).filter(
            User.id == user_id
        ).first()

    def get_by_email(self, db: Session, email: str):

        return db.query(User).filter(
            User.email == email
        ).first()

    def update(
        self,
        db: Session,
        user: User,
        update_data: dict
    ):

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    def delete(self, db: Session, user: User):

        db.delete(user)
        db.commit()

        return True


user_repository = UserRepository()