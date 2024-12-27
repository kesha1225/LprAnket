from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callback_data import SimpleCallbackData


def get_yes_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data=SimpleCallbackData.yes,
                ),
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data=SimpleCallbackData.no,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Начать заново",
                    callback_data=SimpleCallbackData.again,
                )
            ],
        ]
    )
