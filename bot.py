from aiogram import executor
import logging
from loader import dp
import handlers.admin

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
