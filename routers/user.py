from fastapi import APIRouter, HTTPException
from uuid import UUID
from database import users
from schemas.user import UserCreate, UserUpdate, Response
from services.user import user_service


user_router = APIRouter()

@user_router.post("")
def create_user(user_in: UserCreate):
    user = user_service.create_user(user_in)
    return Response(message="User created successfully", data=user)



@user_router.get("")
def get_users():
    return users


@user_router.get("/{id}")
def get_user(id: UUID):
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id: {id} not found")
    return Response(message="User retrieved successfully")



@user_router.put("/{id}")
def update_user(id: UUID, user_in: UserUpdate):
    user = user_service.update_user(id, user_in)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id: {id} not found")
    return Response(message="User updated successfully", data=user)



@user_router.delete("/{id}")
def delete_user(id: UUID):
    user = user_service.delete_user(id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id: {id} not found")
    return Response(message="User deleted successfully")