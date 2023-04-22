import json

import helpers
import common
import schemas

from common import ResponseMessagesValues
from models.base_model import SQLBaseModel
from enums import RoleEnum

import bcrypt
import enum
import typing

from sqlalchemy import Column, String, Boolean


class User(SQLBaseModel):
    __tablename__ = 'users'
    user = Column(String, unique=True)
    password = Column(String)
    verified = Column(Boolean, default=lambda: True)
    enabled = Column(Boolean, default=lambda: True)
    role = Column(String)

    def encrypt_pass(self):
        bytes_pass = self.password.encode('utf-8')
        self.password = bcrypt.hashpw(bytes_pass, bcrypt.gensalt(10)).decode('utf-8')

    def verify_pass(self, obt_pass: str):
        return not not bcrypt.checkpw(obt_pass.encode('utf-8'), self.password.encode('utf-8'))

    def verify_identity(self, token: str):
        token_payload = helpers.decode_token(token)
        requester_id: typing.Optional[int] = token_payload.get('id', None)
        requester_role: typing.Optional[str] = token_payload.get('role', None)
        if requester_id == self.id:
            if requester_role != self.role or not self.enabled or not self.verified:
                raise common.error_handling.NotAllowed(ResponseMessagesValues.NOT_ALLOWED)
        else:
            requester_entity: User = self.query_by_kwargs(first_match=True, id=requester_id)
            if requester_entity.role != RoleEnum.ADMIN.value or requester_role != requester_entity.role or \
                    not requester_entity.enabled or not requester_entity.verified:
                raise common.error_handling.NotAllowed(ResponseMessagesValues.NOT_ALLOWED)

    def dict(self, *args, **kwargs):
        raw_dict: dict = super(User, self).dict(*args, **kwargs)
        user_schema = schemas.UserSchema(**raw_dict)
        return user_schema.dict(*args, **kwargs)

    def json(self, *args, **kwargs):
        raw_dict: dict = super(User, self).json(*args, **kwargs)
        user_schema = schemas.UserSchema(**raw_dict)
        return user_schema.json(*args, **kwargs)


__all__ = ['User']
