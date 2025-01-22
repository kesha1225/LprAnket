from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.constants.callback_data import SimpleCallbackData
from bot.filters.personal_message_filter import OnlyPersonalCallbackFilter
from bot.keyboard.start import get_start_keyboard
from db.models import TGUser

router = Router(name=__name__)
router.callback_query.filter(OnlyPersonalCallbackFilter())


@router.callback_query(F.data == SimpleCallbackData.cancel)
async def cancel_handler(
    callback_query: CallbackQuery, state: FSMContext, current_user: TGUser, bot: Bot
) -> None:
    if await state.get_state() is not None:
        await state.clear()

    await callback_query.answer("Ок, отменено.")
    await callback_query.message.delete()

    bot_message = await bot.send_message(
        chat_id=current_user.tg_id,
        text="Я бот анкеты для связи. Выберите действие.",
        reply_markup=get_start_keyboard(tg_id=current_user.tg_id),
    )

    await state.clear()
    await state.update_data(bot_message=bot_message)
