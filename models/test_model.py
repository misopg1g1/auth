from sqlalchemy import Column, Integer

from config.db_client import Base


class TestModel(Base):
    __tablename__ = "testmodel"
    id = Column(Integer, primary_key=True, index=True)
