from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.constants.callback_data import BroadcastCallbackData, SimpleCallbackData


async def get_broadcast_types_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Все", callback_data=BroadcastCallbackData.broadcast_to_all
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text="Желающие участвовать",
            callback_data=BroadcastCallbackData.broadcast_to_meet_wishers,
        )
    )

    keyboard.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data=SimpleCallbackData.cancel),
    )

    return keyboard.as_markup()


def get_confirm_broadcast_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Разослать", callback_data=BroadcastCallbackData.confirm_broadcast
    )

    keyboard.button(text="Не рассылать", callback_data=SimpleCallbackData.cancel)

    keyboard.adjust(2)
    return keyboard.as_markup()
