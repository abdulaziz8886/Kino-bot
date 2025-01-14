from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import Bot_token
from user.user import user_router
dp = Dispatcher()

bot = Bot(token=Bot_token)
logging.basicConfig(level=logging.INFO)


dp.include_router(user_router)



async def main():
    await bot.send_message(chat_id=5678926023, text="Bot ishga tushdi")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("tugadi")