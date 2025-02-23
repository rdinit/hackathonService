from settings.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def pg_connection() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.pg.url)

    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)