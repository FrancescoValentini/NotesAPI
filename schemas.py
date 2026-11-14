import uuid

from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field


# Generic API response
T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    error: bool = False
    result: T | None = None
    message: str | None = None


# Authentication
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Notes
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = ""


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = None


class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)
