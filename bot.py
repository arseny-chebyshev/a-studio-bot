from aiogram import executor
from aiogram.utils.executor import start_webhook
import logging
from loader import dp, bot
from settings import webhook_url, webhook_path, webapp_host, webapp_port, admin_id
import handlers.admin


async def on_startup(dispatcher):
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
#    await bot.send_message(admin_id, "Starting..")

async def on_shutdown(dispatcher):
    pass
#    await bot.delete_webhook() use it only if you are not using free 30min-and-idle dyno!


def main():
    logging.basicConfig(level=logging.DEBUG)
#    executor.start_polling(dispatcher=dp, on_startup=on_startup)
    start_webhook(dispatcher=dp, webhook_path=webhook_path,
                  skip_updates=True, on_startup=on_startup,
                  on_shutdown=on_shutdown, host=webapp_host,
                  port=webapp_port)
#main()
