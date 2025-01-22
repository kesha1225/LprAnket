from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, BufferedInputFile

from bot.constants.callback_data import SimpleCallbackData
from bot.excel import create_excel_dump
from bot.filters.is_admin import IsAdminCallbackFilter, IsAdminMessageFilter
from bot.filters.personal_message_filter import (
    OnlyPersonalCallbackFilter,
    OnlyPersonalMessageFilter,
)
from bot.time_utils import get_utcnow

router = Router(name=__name__)

router.message.filter(OnlyPersonalMessageFilter(), IsAdminMessageFilter())
router.callback_query.filter(OnlyPersonalCallbackFilter(), IsAdminCallbackFilter())


@router.callback_query(F.data == SimpleCallbackData.excel_dump, StateFilter("*"))
async def excel_dump(callback_query: CallbackQuery):
    now = get_utcnow()
    await callback_query.message.answer_document(
        document=BufferedInputFile(
            file=await create_excel_dump(),
            filename=f"form_dump_{now.strftime("%d_%m_%Y_%H_%M")}.xlsx",
        )
    )

    await callback_query.answer()
