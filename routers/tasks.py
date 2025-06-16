from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from crud import (
    create_task,
    get_tasks,
    get_task_by_id,
    delete_task_by_id,
    update_task_by_id,
)
from schemas import TaskCreate, TaskRead, TaskUpdate
from typing import List

router = APIRouter()


@router.post("/tasks/", response_model=TaskRead)
async def post_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task)


@router.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await get_tasks(db)


@router.get("/users/{task_id}", response_model=TaskRead)
async def read_task_by_id(task_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_task_by_id(task_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{task_id}", response_model=TaskRead)
async def del_user_by_id(task_id: int, db: AsyncSession = Depends(get_db)):
    user = await delete_task_by_id(task_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{task_id}", response_model=TaskRead)
async def update_user(
    task_id: int, user_update: TaskUpdate, db: AsyncSession = Depends(get_db)
):
    user = await update_task_by_id(task_id, user_update, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
