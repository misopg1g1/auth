import datetime
import typing

from enums import RoleEnum

import pydantic


class UserOperationSchema(pydantic.BaseModel):
    requester_user_password: typing.Optional[str] = pydantic.Field(...)


class LoginUserSchema(pydantic.BaseModel):
    user: str = pydantic.Field(...)
    password: str = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': 'gAAAAABkOG6Kxb78NW55YIduu9eoGM7jH6ElVtRdOU1U2M4fLwZhMZeG6xGHMMWjjVrKMkfyjFz8jxbWLoIn7AwxahRqvadfq60EH7vWLewavMypKKf1gU8vZr0PW6Fzx2k-2nUMg3hZ',
                'user': 'user1',
                'password': 'password1',
            }
        }


class CreateUserSchema(LoginUserSchema, UserOperationSchema):
    verify_password: str = pydantic.Field(...)
    role: RoleEnum = pydantic.Field(...)

    class Config:
        use_enum_values = True

        schema_extra = {
            "example": {
                'hash': 'gAAAAABkOFpJfAAGZ0u16F5t5zlgstkWSYvtbfsCuWSouUKHMlCN2-VkU-BYyX9JPNq5sb5SkxwL2HZdnhupO6bZUXqQBXf5sHrVnqDkqqUtsQnHdLK_tO0JKmho6T8CQhOzOMj5EiaK',
                'user': 'user2',
                'password': 'password2',
                'verify_password': 'password2',
                'role': 'ADMIN',
                'requester_user_password': 'password1'

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
