import asyncio
from aiogram import Bot, Dispatcher
from handlers import include_routers

bot = Bot(token="7003052409:AAG1r9XZdCudeVgieMBhvTH8HvSuSCji_n0")
dp = Dispatcher()

async def main():
    include_routers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
