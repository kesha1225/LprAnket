from aiogram.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery, Message


class OnlyPersonalMessageFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id > 0


class OnlyPersonalCallbackFilter(Filter):
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        # callback_query.message is None когда юзер жмет на кнопку которая под сообщением
        # отправленным в чате с via_bot. отследить где он нажал никак нельзя, пиздец
        # НО! если инлайн квери в чат никак не попадет то и кнопок колбека не будет в чате
        # никогда
        if callback_query.message is None:
            return True
        return callback_query.message.chat.id > 0


class OnlyPersonalInlineQueryFilter(Filter):
    async def __call__(self, query: InlineQuery) -> bool:
        return query.chat_type == "sender"
