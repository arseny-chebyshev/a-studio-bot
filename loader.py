from settings import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from requests import Session

bot = Bot(token=bot_token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
session = Session()
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) \
            Gecko/20100101 Firefox/100.0",
           'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'}
session.headers.update(headers)

"""Register middlewares here before starting up the bot"""
# dp.middleware.setup(LoggingMiddleware())

"""Filters"""
# dp.filters_factory.bind(AdminFilter)
