from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user: UserCreate) -> User:
        return self.repository.create_user(user)

    def get_all_users(self) -> list[User]:
        return self.repository.get_all_users()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_user_by_id(user_id)

    def update_user(
        self,
        user_id: int,
        user: UserUpdate
    ) -> User | None:
        return self.repository.update_user(user_id, user)