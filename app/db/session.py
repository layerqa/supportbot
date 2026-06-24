from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

engine = create_async_engine(settings.db.url)
async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
