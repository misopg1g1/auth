from common import error_handling, ResponseMessagesValues
from config.db_client import db_client

import typing

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError


def expire_all_objects(method):
    def wrapper(*args, **kwargs):
        db_client.session.expire_all()
        if response := method(*args, **kwargs):
            return response

    return wrapper


def manage_db_exceptions(method):
    def wrapper(*args, **kwargs):
        try:
            if response := method(*args, **kwargs):
                return response
        except IntegrityError:
            db_client.session.rollback()
            raise error_handling.Conflict(ResponseMessagesValues.USER_ALREADY_EXIST)
        except Exception as e:
            db_client.session.expire_all()
            db_client.session.rollback()
            raise error_handling.AppErrorBaseClass(ResponseMessagesValues.GENERAL_REQUESTS_FAILURE_MESSAGE)

    return wrapper


class SQLBaseModel(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    @classmethod
    @manage_db_exceptions
    @expire_all_objects
    def push_objects(cls, objects):
        db_client.session.add_all(objects)
        db_client.session.commit()

    @classmethod
    @manage_db_exceptions
    @expire_all_objects
    def push_object(cls, obj):
        db_client.session.add(obj)
        db_client.session.commit()

    @classmethod
    @manage_db_exceptions
    @expire_all_objects
    def query_by_kwargs(cls, first_match: bool = False, **kwargs):
        query = db_client.session.query(cls).filter_by(**kwargs)
        return query.first() if first_match else query.all()

    @manage_db_exceptions
    @expire_all_objects
    def update_obj(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        db_client.session.commit()

    @classmethod
    @manage_db_exceptions
    @expire_all_objects
    def query_and_update_by_dicts(cls, query_dict: dict, new_values: dict):
        for obj in db_client.session.query(cls).filter_by(**query_dict).all():
            for key, value in new_values.items():
                obj.__setattr__(key, value)
        db_client.session.commit()

    def dict(self, *args, **kwargs):
        return dict(self.__dict__)

    def json(self, *args, **kwargs):
        return dict(self.__dict__)


__all__ = ['SQLBaseModel']
