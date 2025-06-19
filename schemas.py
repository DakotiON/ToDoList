from pydantic import BaseModel, EmailStr
from typing import List, Optional


class TaskBase(BaseModel):
    title: str
    text: str


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class TaskRead(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserWithTasks(UserRead):
    tasks: List[TaskRead]
