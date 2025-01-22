import logging
import traceback

from aiogram import Bot
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
)
from aiogram.types import LinkPreviewOptions, VideoNote, Voice
from tenacity import TryAgain, retry, stop_after_attempt, wait_fixed

from bot.broadcast.media_group import MediaType

from bot.constants.broadcast import WAIT_BROADCAST, ATTEMPT_COUNT_BROADCAST
from db.crud.user import set_bot_blocked
from db.models import TGUser

logger = logging.getLogger(__name__)


@retry(
    wait=wait_fixed(WAIT_BROADCAST),
    stop=stop_after_attempt(ATTEMPT_COUNT_BROADCAST),
)
async def send_to_user(
    text: str,
    media: list[MediaType],
    bot: Bot,
    user: TGUser,
    link_preview_options: LinkPreviewOptions | None,
):
    if user.is_bot_blocked:
        logger.info(f"Bot blocked for user {user.tg_id}, skip")
        return

    try:
        if not media:
            return await bot.send_message(
                chat_id=user.tg_id, text=text, link_preview_options=link_preview_options
            )

        if isinstance(media[0], Voice):
            return await bot.send_voice(
                chat_id=user.tg_id, voice=media[0].file_id, caption=text
            )
        if isinstance(media[0], VideoNote):
            return await bot.send_video_note(
                chat_id=user.tg_id, video_note=media[0].file_id
            )

        if text:
            media[-1].caption = text

        await bot.send_media_group(chat_id=user.tg_id, media=media)

    except (TelegramForbiddenError, TelegramBadRequest):
        logger.error(traceback.format_exc())
        return await set_bot_blocked(user=user)
    except TelegramAPIError as err:
        logger.warning(
            f"Error sending message to {user.tg_id}: {err}\n{traceback.format_exc()}\n\n{err,}, {err.message=}, {err.args=}"
        )
        raise TryAgain()
