from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user: UserCreate) -> User:
        return self.repository.create_user(user)

    def get_all_users(self) -> list[User]:
        return self.repository.get_all_users()