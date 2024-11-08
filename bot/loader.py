import logging
from aiogram import Bot,Dispatcher
from asgiref.sync import sync_to_async
from aiogram.client.bot import DefaultBotProperties

from set_main.models import BotToken
from bot.handler.users.private_user import user_private_router

logging.basicConfig(level=logging.INFO)

async def get_main_bot_token():
    try:
        main_bot = await sync_to_async(BotToken.objects.get)(user='Admin')
        return main_bot.token
    except BotToken.DoesNotExist:
        raise ValueError("Главный бот не найден в базе данных")

async def on_startup(bot):
    print('Bot is working')

async def on_startup(bot):
    print('I\'m online')

async def main():
    bot_token = await get_main_bot_token()
    bot = Bot(token=bot_token,default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.include_router(user_private_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)