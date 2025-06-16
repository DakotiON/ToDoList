from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Task
from schemas import TaskCreate, TaskUpdate
from typing import List


async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(title=task.title, text=task.text)
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
