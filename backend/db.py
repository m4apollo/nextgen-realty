from sqlmodel import create_engine, SQLModel, Session
from backend.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Synchronous engine for SQLite
sync_engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Async engine for production databases
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("sqlite", "sqlite+aiosqlite"),
    echo=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_session() -> Session:
    with Session(sync_engine) as session:
        yield session