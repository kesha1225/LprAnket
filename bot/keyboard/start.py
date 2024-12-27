from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.admins import ADMINS
from bot.constants.callback_data import SimpleCallbackData


def get_start_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Заполнить анкету",
                callback_data=SimpleCallbackData.start_form,
            )
        ]
    ]

    if tg_id in ADMINS:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="📤 Выгрузка результатов",
                    callback_data=SimpleCallbackData.excel_dump,
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
