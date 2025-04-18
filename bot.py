import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import mainHandlers, adminHandlers

bot = Bot(token=config.TOKEN)

async def main():
    dp = Dispatcher()
    
    dp.include_routers(adminHandlers.adminrt, mainHandlers.mainrt)
    
    print("poling started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())