from typing import Optional

from pydantic import BaseModel, EmailStr


class TaskCreate(BaseModel):
    title: str
    text: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class TaskRead(BaseModel):
    id: int
    title: str
    text: str

    class Config:
        orm_mode = True
