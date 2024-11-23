from schemas.user import UserInCreate, UserInUpdate
from models.user import User
from repositories.user import UserRepository
from uuid import UUID


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def add(self, user: UserInCreate) -> User:
        return self.user_repository.add(user)

    def get_all(self) -> list[User]:
        return self.user_repository.get_all()

    def get_by_id(self, user_id: UUID) -> User:
        return self.user_repository.get_by_id(user_id)

    def update(self, user_id: UUID, user_new: UserInUpdate) -> User:
        return self.user_repository.update(user_id, user_new)

    def delete(self, user_id: UUID) -> None:
        return self.user_repository.delete(user_id)

    def change_password(self, user_passwords, user) -> User:
        return self.user_repository.change_password(user_passwords, user)

    def add_image(self, user_id: UUID, image_path: str) -> User:
        return self.user_repository.add_image(user_id, image_path)
