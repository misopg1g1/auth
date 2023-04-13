from models import User, RoleEnum
from schemas import UserSchema

from fastapi import APIRouter, Depends

session_router = APIRouter(prefix="/session", tags=["Session"])


@session_router.post("/create_user")
def create_user(user_schema: UserSchema):
    new_user = User(**user_schema.dict())
    User.push_object(new_user)
    return 'usuario creado'


__all__ = ["session_router"]
