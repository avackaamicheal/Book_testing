import uuid
from typing import Optional
from schemas.user import UserCreate, UserUpdate, User
from database import users

class UserService:

    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        user_id = uuid.uuid4()
        user = User(id=user_id, **user_data.model_dump())
        users[user_id] = user
        return user
    

    @staticmethod
    def get_user(user_id: uuid.UUID) -> Optional[User]:
        return users.get(user_id)
    
    @staticmethod
    def update_user(user_id: uuid.UUID, user_data: UserUpdate) -> Optional[User]:
        if user_id in users:
            updated_user = User(id=user_id, **user_data.model_dump())
            users[user_id] = updated_user
            return updated_user
        return None

    def delete_user(self, user_id: uuid.UUID) -> Optional[User]:
        return users.pop(user_id, None)

user_service = UserService()