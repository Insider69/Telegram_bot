import asyncio
import configure
from aiogram import Bot, Dispatcher
from commands import other, keyboards, questionaire, user_commands
from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import AntiFloodMiddleware
from aiogram.client.default import DefaultBotProperties
import sys
print(sys.version_info)



async def main():
    bot = Bot(configure.config['token'], default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.message.middleware(CheckSubscription())
    dp.message.middleware(AntiFloodMiddleware())
    
    dp.include_routers(
        other.bp,
        keyboards.bp,
        questionaire.bp,
        user_commands.bp
    )

    print('Bot started ✅')
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())