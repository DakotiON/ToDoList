from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Зависимость для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
