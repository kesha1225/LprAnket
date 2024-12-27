from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.constants.callback_data import SimpleCallbackData
from bot.constants.state import FormGroup
from bot.convertor import get_bool_from_callback_data
from bot.deleter import delete_previous_bot_message, delete_message_with_suppress
from bot.keyboard.again import get_again_keyboard
from bot.keyboard.empty import get_skip_keyboard
from bot.keyboard.yes_no import get_yes_no_keyboard
from db.crud.form import create_new_form
from db.models import TGUser

router = Router(name=__name__)


@router.callback_query(F.data == SimpleCallbackData.start_form)
async def start_form_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback_query.answer()
    await state.set_state(FormGroup.name)

    bot_message = await callback_query.message.answer(
        "Как вас зовут?", reply_markup=get_again_keyboard()
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await state.update_data(bot_message=bot_message)

    await delete_message_with_suppress(callback_query.message)


@router.message(StateFilter(FormGroup.name))
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(data={FormGroup.name.state: message.text})

    bot_message = await message.answer(
        "Откуда вы (из какого региона)?",
        reply_markup=get_again_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=message.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.region)

    await delete_message_with_suppress(message)


@router.message(StateFilter(FormGroup.region))
async def region_handler(message: Message, state: FSMContext):
    await state.update_data(data={FormGroup.region.state: message.text})

    bot_message = await message.answer(
        "Хотите ли вы получать уведомления о новых мероприятиях?",
        reply_markup=get_yes_no_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=message.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.notify)
    await delete_message_with_suppress(message)


@router.callback_query(StateFilter(FormGroup.notify))
async def notify_form_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(
        data={
            FormGroup.notify.state: get_bool_from_callback_data(
                data=callback_query.data
            )
        }
    )

    bot_message = await callback_query.message.answer(
        "Хотите ли вы встретиться с либертарианцами вашего города?",
        reply_markup=get_yes_no_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.meetings)

    await callback_query.answer()
    await delete_message_with_suppress(callback_query.message)


@router.callback_query(StateFilter(FormGroup.meetings))
async def meetings_form_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(
        data={
            FormGroup.meetings.state: get_bool_from_callback_data(
                data=callback_query.data
            )
        }
    )

    bot_message = await callback_query.message.answer(
        "Хотите ли вы заниматься около-политической активностью без привязки к какой-либо организации",
        reply_markup=get_yes_no_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.near_politic)

    await callback_query.answer()
    await delete_message_with_suppress(callback_query.message)


@router.callback_query(StateFilter(FormGroup.near_politic))
async def meetings_form_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(
        data={
            FormGroup.near_politic.state: get_bool_from_callback_data(
                data=callback_query.data
            )
        }
    )

    bot_message = await callback_query.message.answer(
        "Хотите ли вы вступить в ЛПР или стать сторонником организации?",
        reply_markup=get_yes_no_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.lpr_join)

    await callback_query.answer()
    await delete_message_with_suppress(callback_query.message)


@router.callback_query(StateFilter(FormGroup.lpr_join))
async def lpr_join_form_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(
        data={
            FormGroup.lpr_join.state: get_bool_from_callback_data(
                data=callback_query.data
            )
        }
    )

    bot_message = await callback_query.message.answer(
        "Идеи, послания, пожелания:",
        reply_markup=get_skip_keyboard(),
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await state.update_data(bot_message=bot_message)
    await state.set_state(FormGroup.other)

    await callback_query.answer()
    await delete_message_with_suppress(callback_query.message)


@router.message(StateFilter(FormGroup.other))
async def other_text_handler(message: Message, state: FSMContext, current_user: TGUser):
    if message.text is None:
        return await message.answer(
            "В качестве пожеланий можно отправить только текст."
        )

    await state.update_data(data={FormGroup.other.state: message.text})

    await message.answer(
        "Результат сохранён. Спасибо за прохождение!", reply_markup=get_again_keyboard()
    )
    await delete_previous_bot_message(state=state, bot=message.bot)

    await create_new_form(tg_id=current_user.tg_id, form_dict=await state.get_data())
    await state.clear()
    await delete_message_with_suppress(message)


@router.callback_query(StateFilter(FormGroup.other))
async def other_cb_text_handler(
    callback_query: CallbackQuery, state: FSMContext, current_user: TGUser
):
    await state.update_data(data={FormGroup.other.state: None})

    await callback_query.message.answer(
        "Результат сохранён. Спасибо за прохождение!", reply_markup=get_again_keyboard()
    )
    await delete_previous_bot_message(state=state, bot=callback_query.bot)
    await callback_query.answer()

    await create_new_form(tg_id=current_user.tg_id, form_dict=await state.get_data())

    await state.clear()
    await delete_message_with_suppress(callback_query.message)
