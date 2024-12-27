import asyncio
import logging

from bot.bot import run_bot
from bot.constants.log import LOG_FILENAME

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME)
    logging.info("Bot starting...")
    asyncio.run(run_bot())
