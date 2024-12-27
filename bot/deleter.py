import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InaccessibleMessage


async def delete_previous_bot_message(state: FSMContext, bot: Bot):
    bot_message = await state.get_value("bot_message")
    if bot_message:
        await bot.delete_message(
            chat_id=bot_message.chat.id, message_id=bot_message.message_id
        )


async def delete_message_with_suppress(message: Message | InaccessibleMessage | None):
    if not isinstance(message, Message):
        return

    try:
        await message.delete()
    except Exception as e:
        logging.error(f"cant delete {message.message_id} {e}")
