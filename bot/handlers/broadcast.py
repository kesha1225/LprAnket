import asyncio

import aiogram
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_media_group import media_group_handler

from bot.broadcast.broadcaster import (
    get_user_for_broadcast_by_choice_type,
    broadcast_to_players,
)
from bot.deleter import delete_previous_bot_message
from bot.filters.is_admin import IsAdminCallbackFilter, IsAdminMessageFilter
from bot.filters.personal_message_filter import (
    OnlyPersonalCallbackFilter,
    OnlyPersonalMessageFilter,
)

from bot.constants.callback_data import BroadcastCallbackData
from bot.constants.state import BroadcastForm
from bot.keyboard.broadcast import (
    get_broadcast_types_keyboard,
    get_confirm_broadcast_keyboard,
)
from db.models import TGUser

router = Router(name=__name__)
router.message.filter(OnlyPersonalMessageFilter(), IsAdminMessageFilter())
router.callback_query.filter(OnlyPersonalCallbackFilter(), IsAdminCallbackFilter())


@router.callback_query(F.data == BroadcastCallbackData.start_broadcast)
async def start_broadcast_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    if await state.get_state() is not None:
        await state.clear()

    await callback_query.message.edit_text(
        text="Выберите тип пользователей для рассылки.\n\n<i>Желающие участвовать - это те, кто в анкете ответили,"
        " что хотят получать уведомления о новых мероприятиях или встретиться "
        "с либертарианцами вашего города или хотят заниматься около-политической активностью без "
        "привязки к какой-либо организации или хотят ли вы вступить в ЛПР или стать сторонником организации</i>",
        reply_markup=await get_broadcast_types_keyboard(),
        parse_mode=ParseMode.HTML,
    )
    await callback_query.answer()
    await state.set_state(BroadcastForm.choice_type)


@router.callback_query(StateFilter(BroadcastForm.choice_type))
async def choice_type_broadcast_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.update_data({"type": callback_query.data})

    bot_message = await callback_query.message.edit_text(
        text="Отправьте сообщение для рассылки.", reply_markup=None
    )
    await state.update_data(bot_message=bot_message)
    await callback_query.answer()
    await state.set_state(BroadcastForm.input_message)


@router.message(StateFilter(BroadcastForm.input_message))
@media_group_handler(only_album=False)
async def album_handler(
    messages: list[Message], state: FSMContext, bot: aiogram.Bot, current_user: TGUser
) -> None:
    await bot.delete_messages(
        chat_id=current_user.tg_id,
        message_ids=[message.message_id for message in messages],
    )
    await delete_previous_bot_message(state=state, bot=bot)

    await state.update_data({"messages": messages})

    choice_type = (await state.get_data())["type"]

    users_to_send_count = len(
        await get_user_for_broadcast_by_choice_type(choice_type=choice_type)
    )

    await messages[-1].answer(
        text=f"Разослать данное сообщение на {users_to_send_count} пользователей?",
        reply_markup=get_confirm_broadcast_keyboard(),
    )

    await state.set_state(BroadcastForm.confirm)


@router.callback_query(StateFilter(BroadcastForm.confirm))
async def send_broadcast_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    data = await state.get_data()
    await state.clear()

    messages = data["messages"]
    choice_type = data["type"]

    users = await get_user_for_broadcast_by_choice_type(choice_type=choice_type)

    asyncio.create_task(broadcast_to_players(users=users, messages=messages))
    await callback_query.answer()

    await callback_query.message.delete()
