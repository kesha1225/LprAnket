from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from bot.constants.admins import ADMINS
from db.models import TGUser


class OnlyAdmin(Filter):
    async def __call__(
        self,
        callback_query: CallbackQuery,
        current_user: TGUser,
    ) -> bool:
        return current_user.tg_id in ADMINS
