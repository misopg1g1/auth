import typing
import common
import models
import helpers
import enums
import schemas

from schemas import LoginUserSchema, CreateUserSchema

import json
import uuid

from fastapi import APIRouter, Depends, Response

session_router = APIRouter(prefix="/session", tags=["Session"])


@session_router.post("/create_user")
def create_user(new_user_schema: CreateUserSchema, token: str = Depends(common.token_schema)):
    new_user_dict = dict(filter(lambda kv: kv[0] not in ["verify_password", "requester_user_password"],
                                new_user_schema.dict().items()))
    new_user_instance = models.User(**new_user_dict)
    id = str(uuid.uuid4())
    new_user_instance.id = id
    if new_user_schema.password != new_user_schema.verify_password:
        raise common.error_handling.Conflict(common.response_messages.ResponseMessagesValues.PASSWORD_MISSMATCH)
    new_user_instance.verify_identity(token)
    new_user_instance.encrypt_pass()
    models.User.push_object(new_user_instance)
    return {"id": id}


@session_router.delete("/delete/{user_id}")
def delete_user(user_id: str, response: Response, token: str = Depends(common.token_schema)):
    target_instance: typing.Optional[models.User] = models.User.query_by_kwargs(first_match=True, id=user_id)
    if not target_instance:
        raise common.error_handling.ObjectNotFound(common.response_messages.ResponseMessagesValues.OBJECT_NOT_FOUND)
    if target_instance.id == helpers.decode_token(token).get("id"):
        raise common.error_handling.NotAllowed(common.response_messages.ResponseMessagesValues.CANNOT_DELETE_SAME_USER)
    target_instance.verify_identity(token)
    if models.User.delete_by_kwargs(first_match=True, id=user_id):
        response.status_code = 204


@session_router.get("/refresh_token")
def refresh_token(token: str = Depends(common.token_schema)):
    token_payload = helpers.decode_token(token)
    user_instance: typing.Optional[models.User]
    if (user_id := token_payload.get("id", None)) and \
            (user_instance := models.User.query_by_kwargs(first_match=True, id=user_id)):
        user_instance.verify_identity(token)
        return {
            "access_token": helpers.generate_token(json.loads(user_instance.json(exclude={'password'}))),
            "token_type": "bearer"
        }
    else:
        raise common.error_handling.ObjectNotFound(common.response_messages.ResponseMessagesValues.OBJECT_NOT_FOUND)


@session_router.get("/verify_token")
def verify_token(resp: Response, token: str = Depends(common.token_schema)):
    token_payload = helpers.decode_token(token)
    user_instance: typing.Optional[models.User]
    if (user_id := token_payload.get("id", None)) and \
            (user_instance := models.User.query_by_kwargs(first_match=True, id=user_id)):
        user_instance.verify_identity(token)
        return json.loads(user_instance.json(exclude={'password'}))
    else:
        raise common.error_handling.ObjectNotFound(common.response_messages.ResponseMessagesValues.OBJECT_NOT_FOUND)


@session_router.post("/verify_roles")
def verify_roles(roles_schema: schemas.RolesSchema, response: Response, token: str = Depends(common.token_schema)):
    token_payload = helpers.decode_token(token)
    user_instance: typing.Optional[models.User]
    if (user_id := token_payload.get("id", None)) and \
            (user_instance := models.User.query_by_kwargs(first_match=True, id=user_id)):
        user_instance.verify_identity(token)
        if user_instance.role in list(map(lambda r: r, roles_schema.roles)):
            response.status_code = 204
        else:
            raise common.error_handling.Forbidden(common.response_messages.ResponseMessagesValues.DIFFERENT_ROLE)
    else:
        raise common.error_handling.ObjectNotFound(common.response_messages.ResponseMessagesValues.OBJECT_NOT_FOUND)


@session_router.post("/login", response_model=schemas.LoginResponseSchema)
def login(user_schema: LoginUserSchema):
    user_instance: typing.Optional[models.User]
    if user_instance := models.User.query_by_kwargs(first_match=True, user=user_schema.user):
        if not user_instance.verified:
            raise common.error_handling.NotAllowed(common.response_messages.ResponseMessagesValues.NOT_VERIFIED)
        if not user_instance.enabled:
            raise common.error_handling.NotAllowed(common.response_messages.ResponseMessagesValues.NOT_ENABLED)
        if not user_instance.verify_pass(user_schema.password):
            raise common.error_handling.NotAllowed(common.response_messages.ResponseMessagesValues.NOT_ALLOWED)
        return {
            "access_token": helpers.generate_token(json.loads(user_instance.json(exclude={'password'}))),
            "token_type": "bearer",
            "data": json.loads(user_instance.json(exclude={'password'}))
        }

    else:
        raise common.error_handling.ObjectNotFound(common.response_messages.ResponseMessagesValues.OBJECT_NOT_FOUND)


__all__ = ["session_router"]
