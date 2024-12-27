from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.schemas import UserMiddlewareStruct
from db.crud.user import extract_from_middleware


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        current_user = await extract_from_middleware(
            user_struct=UserMiddlewareStruct.from_aiogram_event(event=event)
        )
        data["current_user"] = current_user

        return await handler(event, data)
