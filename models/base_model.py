from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase

from config.db_client import db_client


def expire_all_objects(method):
    def wrapper(*args, **kwargs):
        db_client.session.expire_all()
        method(*args, **kwargs)

    return wrapper


class BaseModel(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable= True)

    @classmethod
    def push_objects(cls, objects):
        db_client.session.add_all(objects)
        db_client.session.commit()

    @classmethod
    def push_object(cls, obj):
        db_client.session.add(obj)
        db_client.session.commit()

    @classmethod
    @expire_all_objects
    def query_by_kwargs(cls, first_match: bool = False, **kwargs):
        query = db_client.session.query(cls).filter_by(**kwargs)
        return query.first() if first_match else query.all()

    def update_obj(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        db_client.session.commit()

    @classmethod
    @expire_all_objects
    def query_and_update_by_dicts(cls, query_dict: dict, new_values: dict):
        for obj in db_client.session.query(cls).filter_by(**query_dict).all():
            for key, value in new_values.items():
                obj.__setattr__(key, value)
        db_client.session.commit()


__all__ = ['BaseModel']
