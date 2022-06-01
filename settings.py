import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
post_channel = os.getenv('POST_CHANNEL_ID')
dikidi_org = os.getenv('DIKIDI_ORG')
heroku_app = os.getenv('HEROKU_APP')
webhook_host = f'https://{heroku_app}.herokuapp.com'
webhook_path = f'/webhook/{bot_token}'
webhook_url = f'{webhook_host}{webhook_path}'
webapp_host = '0.0.0.0'
webapp_port = os.getenv('PORT', default=8000)
