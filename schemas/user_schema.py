import typing

from models import RoleEnum

import pydantic


class UserSchema(pydantic.BaseModel):
    user: str = pydantic.Field(...)
    password: str = pydantic.Field(...)
    role: RoleEnum = pydantic.Field(...)

    class Config:
        use_enum_values = True


__all__ = ['UserSchema']
