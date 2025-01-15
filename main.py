from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import Bot_token
from user.user import user_router

logging.basicConfig(level=logging.INFO)

async def main():
    # `async with` yordamida Bot sessiyasini boshqarish
    async with Bot(token=Bot_token) as bot:
        dp = Dispatcher()
        dp.include_router(user_router)

        try:
            # Bot ishga tushganini bildirish
            await bot.send_message(chat_id=5678926023, text="Bot ishga tushdi")
            # Pollingni boshlash
            await dp.start_polling(bot)
        except asyncio.CancelledError:
            logging.info("Polling to'xtatildi.")
        finally:
            logging.info("Polling va sessiya tugatildi.")
            # Qo'shimcha ulanishlarni yopish
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Dastur to'xtatildi.")
