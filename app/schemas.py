from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: Union[str, None] = None


class CreateUser(UserBase):
    password: str


class UpdateUser(UserBase):
    pass


class Login(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    new_password2: str


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None
    done: bool = False


class Task(TaskBase):
    id: int
    owner_id: int
    order: int = 0
    created_at: datetime
    updated_at: datetime


class CreateTask(TaskBase):
    pass


class UpdateTask(TaskBase):
    order: int


class CreateSharedTask(BaseModel):
    shared_with_email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
