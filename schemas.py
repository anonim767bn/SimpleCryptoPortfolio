from pydantic import BaseModel, validator
from uuid import UUID
from config import SPECIAL_SYMBOLS


class UUIDmixin:
    id: UUID


class Portfolio(BaseModel, UUIDmixin):
    name: str


class User(BaseModel):
    username: str


class UserCreate(User):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        elif not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        elif not any(char.isupper() for char in v):
            raise ValueError(
                'Password must contain at least one uppercase letter')
        elif not any(char.islower() for char in v):
            raise ValueError(
                'Password must contain at least one lowercase letter')
        elif not any(char in SPECIAL_SYMBOLS for char in v):
            raise ValueError(
                'Password must contain at least one special character')
        return v


class UserDisplay(User, UUIDmixin):
    pass
