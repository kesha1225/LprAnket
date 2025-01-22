from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.schemas import UserMiddlewareStruct
from db.models import FormDB
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
        user.is_bot_blocked = False
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


@with_session
async def set_bot_blocked(user: TGUser, session: AsyncSession):
    user.is_bot_blocked = True

    await session.commit()


@with_session
async def get_all_users_for_broadcast(session: AsyncSession) -> list[TGUser]:
    return list((await session.execute(select(TGUser))).scalars().all())


@with_session
async def get_meet_wishers_for_broadcast(session: AsyncSession) -> list[TGUser]:
    statement = (
        select(TGUser)
        .join(FormDB, TGUser.tg_id == FormDB.user_tg_id)
        .where(
            or_(
                FormDB.notify == True,
                FormDB.meetings == True,
                FormDB.near_politic == True,
                FormDB.lpr_join == True,
            )
        )
        .distinct()
    )

    return list((await session.execute(statement)).scalars().all())
