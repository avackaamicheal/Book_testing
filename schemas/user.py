from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class User(BaseModel):
    id:UUID
    name: str
    email:EmailStr
    age:int

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int

class Users(BaseModel):
    users:list[User]

class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[User | Users] = None