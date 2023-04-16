import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"
    TRANSPORTER = "TRANSPORTER"
    MARKETING = "MARKETING"
    CLIENT = "CLIENT"


__all__ = ['RoleEnum']
