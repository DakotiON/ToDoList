from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from crud import (
    create_task,
    get_tasks,
    get_task_by_id,
    delete_task_by_id,
    update_task_by_id,
    create_user,
    get_user_by_id,
    get_users,
    get_all_user_tasks,
)
from models import User
from schemas import TaskCreate, TaskRead, TaskUpdate, UserRead, UserCreate
from typing import List

router = APIRouter()


# USERS
@router.post("/users/", response_model=UserRead)
async def create_user_view(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@router.get("/users/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_all_user_tasks(user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="Task with this user_id not found")
    return user


# TASKS
@router.post("/tasks/", response_model=TaskRead, status_code=201)
async def post_task(task: TaskCreate, db: AsyncSession = Depends(get_db)) -> TaskRead:
    """
    Создает новую задачу, привязанную к пользователю.

    - Проверяет существование пользователя
    - Создает задачу через CRUD-функцию
    """
    # 1. Проверка существования пользователя
    user = await db.get(User, task.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {task.user_id} not found",
        )

    # 2. Создание задачи (user_id уже содержится в task)
    created_task = await create_task(db=db, task=task)
    return created_task


@router.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await get_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task_by_id(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(task_id, db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", response_model=TaskRead)
async def delete_task_view(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await delete_task_by_id(task_id, db)
    if task is None:
        raise HTTPException(status_code=404, detail="User not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task_view(
    task_id: int, user_update: TaskUpdate, db: AsyncSession = Depends(get_db)
):
    task = await update_task_by_id(task_id, user_update, db)
    if task is None:
        raise HTTPException(status_code=404, detail="User not found")
    return task
