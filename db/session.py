from typing import Callable, Awaitable, Any
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from bot.constants.env import DB_URL

engine = create_async_engine(DB_URL)
async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


def with_session(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, session: AsyncSession | None = None, **kwargs):
        should_close = False
        if session is None:
            should_close = True
            session = async_session_factory()

        try:
            return await func(*args, session=session, **kwargs)
        finally:
            if should_close:
                await session.close()

    return wrapper
