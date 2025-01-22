from aiogram.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery, Message

from bot.constants.admins import ADMINS


class IsAdminMessageFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS


class IsAdminCallbackFilter(Filter):
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.from_user.id in ADMINS


class IsAdminInlineQueryFilter(Filter):
    async def __call__(self, query: InlineQuery) -> bool:
        return query.from_user.id in ADMINS
