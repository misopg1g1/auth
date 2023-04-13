from config import AppConfigValues

import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DatabaseClient:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url, echo=True)
        self.session = Session(self.engine, autoflush=True)


db_client = DatabaseClient(AppConfigValues.DB_URL)
