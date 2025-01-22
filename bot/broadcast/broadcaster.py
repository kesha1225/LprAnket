import logging
import time
import traceback
import typing

from aiogram.types import Message
from asyncio_pool import AioPool

from bot.broadcast.media_group import create_input_media_data_from_input
from bot.broadcast.smart_send import send_to_user
from bot.constants.callback_data import BroadcastCallbackData
from db.crud.user import get_all_users_for_broadcast, get_meet_wishers_for_broadcast
from db.models import TGUser

logger = logging.getLogger(__name__)


async def broadcast_to_players(
    users: list[TGUser],
    messages: list[Message],
):
    start = time.time()
    text, media, link_preview_options = create_input_media_data_from_input(
        messages=messages
    )
    async with AioPool(size=7) as pool:
        for user in users:
            try:
                await pool.spawn(
                    send_to_user(
                        text=text,
                        media=media,
                        bot=messages[-1].bot,
                        user=user,
                        link_preview_options=link_preview_options,
                    )
                )
            except Exception as e:
                logger.error(
                    f"send_to_user error username={user.username},"
                    f" tg_id={user.tg_id} - {e}\n{traceback.format_exc()}"
                )

    logger.info(f"broadcast_to_players finished {time.time() - start}")


async def get_user_for_broadcast_by_choice_type(
    choice_type: BroadcastCallbackData,
) -> list[TGUser] | typing.NoReturn:
    if choice_type == BroadcastCallbackData.broadcast_to_all:
        return await get_all_users_for_broadcast()
    elif choice_type == BroadcastCallbackData.broadcast_to_meet_wishers:
        return await get_meet_wishers_for_broadcast()
    else:
        raise ValueError(f"no such type {choice_type}")
