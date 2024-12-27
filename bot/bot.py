from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.constants.env import BOT_TOKEN
from bot.handlers import start_router, form_router, bad_router, admin_router
from bot.middlewares.user import UserMiddleware

dp = Dispatcher()
dp.include_routers(start_router, form_router, admin_router, bad_router)
dp.message.outer_middleware(UserMiddleware())
dp.callback_query.outer_middleware(UserMiddleware())

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def run_bot():
    await bot.set_my_commands(
        commands=[BotCommand(command="start", description="Начать")]
    )
    await dp.start_polling(bot)
