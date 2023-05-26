import logging
import asyncio
from aiogram import Bot, Dispatcher

from handlers import comands, documents, states
from config_reader import config


# Ведение логов
logging.basicConfig(level=logging.INFO)

# функция для запуска бота
async def main():
    # токен скрыт через настройки конфига
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(comands.router, documents.router, states.router)
    # игнорируем обновления, которые были в чате
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
