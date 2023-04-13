import enum
from models.base_model import BaseModel
from sqlalchemy import Column, String, Boolean


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"
    TRANSPORTER = "TRANSPORTER"
    MARKETING = "MARKETING"
    CLIENT = "CLIENT"


class User(BaseModel):
    __tablename__ = 'users'
    user = Column(String)
    password = Column(String)
    status = Column(Boolean, default=lambda: True)
    role = Column(String)


__all__ = ['RoleEnum', 'User']
