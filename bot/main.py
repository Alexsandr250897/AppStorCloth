import asyncio
import logging

from aiogram import Bot, Dispatcher
from bot.handlers import router
from bot.admin import admin

from bot.database.models import async_main
from bot.config import BOT_TOKEN


async def main():
    await async_main()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router,admin)
    await dp.start_polling(bot)

if __name__== '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot offline')
