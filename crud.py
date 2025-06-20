from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Task, User
from schemas import TaskCreate, TaskUpdate, UserCreate
from typing import List

from fastapi import HTTPException, status


# USERS
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # Проверка существования email
    existing_user = await db.execute(select(User).where(User.email == user.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Создание пользователя
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


"Функция используется только если не ставим lazy=selectin"
# async def get_all_user_tasks(user_id: int, db: AsyncSession) -> Task | None:
#    result = await db.execute(select(Task).where(Task.user_id == user_id))
#    return result.scalars().all()


# TASKS
async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(
        title=task.title,
        text=task.text,
        user_id=task.user_id,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(db: AsyncSession) -> List[Task]:
    result = await db.execute(select(Task))
    return result.scalars().all()


async def get_task_by_id(task_id: int, db: AsyncSession) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def delete_task_by_id(task_id: int, db: AsyncSession) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        return None

    await db.delete(task)
    await db.commit()
    return task  # Возвращаем удалённого пользователя


async def update_task_by_id(
    task_id: int, new_data: TaskUpdate, db: AsyncSession
) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        return None  # пользователь не найден

    if new_data.text is not None:
        task.text = new_data.text
    if new_data.title is not None:
        task.title = new_data.title

    await db.commit()
    await db.refresh(task)
    return task
###