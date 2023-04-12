from config import AppConfigValues

import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase


class Base(DeclarativeBase):
    pass


class DatabaseClient:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url, echo=True)
        self.session = Session(self.engine)

    def push_objects(self, objects: typing.List[Base]):
        self.session.add_all(objects)


db_client = DatabaseClient(AppConfigValues.DB_URL)
