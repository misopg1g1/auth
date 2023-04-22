import datetime
import typing

from enums import RoleEnum

import pydantic


class LoginUserSchema(pydantic.BaseModel):
    user: str = pydantic.Field(...)
    password: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': 'gAAAAABkPv5wM9DiujiucuuKmrgtpG2FFi2v81lmzT4qX6yDsVqdYIQWM2RPlTUFSXiOATggPVC4XjSx7cHgJGXBtEIYdMWtjmseyrSno0PiNfJeZw9XW8snoOrwg7YruNf8RJL4CFGH',
                'user': 'user1',
                'password': 'password1',
            }
        }


class CreateUserSchema(LoginUserSchema):
    verify_password: str = pydantic.Field(...)
    role: RoleEnum = pydantic.Field(default=RoleEnum.SELLER)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': 'gAAAAABkPv6ar3w3MmJ4BwxRxfWupoj-9XXX5Nfr4T8jza8p9BxXGnNHvmy4SwkumgwBWI9IFt3REOhr0id2u9MyxQszzvh5jLvqCbdjdMdO45UoSxkqmFxTtCpSqKzIFBfDKK4vwTgr',
                'user': 'user2',
                'password': 'password2',
                'verify_password': 'password2',
                'role': 'ADMIN'

            }
        }


class UserSchemaWithoutPassword(pydantic.BaseModel):
    id: typing.Optional[int]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    user: str
    verified: bool
    enabled: bool
    role: str

    class Config:
        use_enum_values = True


class UserSchema(UserSchemaWithoutPassword):
    password: str

    class Config:
        use_enum_values = True


class LoginResponseSchema(pydantic.BaseModel):
    access_token: str
    token_type: str
    data: UserSchemaWithoutPassword


__all__ = ['LoginUserSchema', 'CreateUserSchema', 'UserSchema', 'LoginResponseSchema']
