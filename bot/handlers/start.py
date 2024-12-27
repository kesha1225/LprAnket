from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.constants.callback_data import SimpleCallbackData
from bot.deleter import delete_previous_bot_message, delete_message_with_suppress
from bot.keyboard.start import get_start_keyboard
from db.models import TGUser

router = Router(name=__name__)


@router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, state: FSMContext, current_user: TGUser):
    bot_message = await message.answer(
        "Я бот анкеты для связи. Выберите действие.",
        reply_markup=get_start_keyboard(tg_id=current_user.tg_id),
    )
    await delete_previous_bot_message(state=state, bot=message.bot)

    await state.clear()
    await state.update_data(bot_message=bot_message)
    await delete_message_with_suppress(message)


@router.callback_query(F.data == SimpleCallbackData.again, StateFilter("*"))
async def cb_start_handler(
    callback_query: CallbackQuery, state: FSMContext, current_user: TGUser
):
    bot_message = await callback_query.message.answer(
        "Я бот анкеты для связи. Выберите действие.",
        reply_markup=get_start_keyboard(tg_id=current_user.tg_id),
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)

    await state.clear()

    await state.update_data(bot_message=bot_message)

    await delete_message_with_suppress(callback_query.message)
