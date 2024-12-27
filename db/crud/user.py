from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.schemas import UserMiddlewareStruct
from db.models.user import TGUser
from db.session import with_session


@with_session
async def extract_from_middleware(
    user_struct: UserMiddlewareStruct,
    session: AsyncSession,
):
    user = (
        await session.execute(select(TGUser).where(TGUser.tg_id == user_struct.tg_id))
    ).scalar_one_or_none()

    if user:
        user.username = user_struct.username
        user.first_name = user_struct.first_name
        user.last_name = user_struct.last_name
        user.is_bot_blocked = True
    else:
        user = TGUser(
            tg_id=user_struct.tg_id,
            username=user_struct.username,
            first_name=user_struct.first_name,
            last_name=user_struct.last_name,
        )
        session.add(user)

    await session.commit()
    return user
