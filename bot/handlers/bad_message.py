from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router(name=__name__)


@router.message(StateFilter("*"))
async def bad_handler(message: Message):
    await message.delete()
