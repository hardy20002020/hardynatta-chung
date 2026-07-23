from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_user(self, user: UserCreate) -> User:

        existing_user = (
            self.db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered")


        db_user = User(
            name=user.name,
            email=user.email,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user


    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()


    def get_user_by_id(self, user_id: int) -> User | None:

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )


    def update_user(
        self,
        user_id: int,
        user: UserUpdate
    ) -> User | None:

        db_user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if db_user is None:
            return None


        db_user.name = user.name
        db_user.email = user.email


        self.db.commit()
        self.db.refresh(db_user)

        return db_user


    def delete_user(self, user_id: int) -> bool:

        db_user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if db_user is None:
            return False


        self.db.delete(db_user)
        self.db.commit()

        return True