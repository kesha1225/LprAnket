from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callback_data import SimpleCallbackData


def get_again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Начать заново",
                    callback_data=SimpleCallbackData.again,
                )
            ]
        ]
    )
