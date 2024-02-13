import os
import dotenv
import logging
import asyncio


from core.modules.telegram_bot import TelegramBot
from core.modules.openai_helper import OpenAIHelper
from core.db.db import Database


def main():
    dotenv.load_dotenv()
    
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

    logger = logging.getLogger(__name__)
       
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
        exit(1)
        
    model = os.environ.get('OPENAI_MODEL', 'gpt-4-0125-preview')
        
    openai_config = {
        'api_key': os.environ['OPENAI_API_KEY'],
        'show_usage': os.environ.get('SHOW_USAGE', 'false').lower() == 'true',
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'assistant_prompt': os.environ.get('ASSISTANT_PROMPT', 'You are a helpful assistant.'),
        'temperature': float(os.environ.get('TEMPERATURE', 1.0)),
        'model': model,
    }
        
    telegram_config = {
        'token': os.environ['TELEGRAM_BOT_TOKEN'],
        'admin_user_ids': os.environ.get('ADMIN_USER_IDS', '-'),
        'bot_language': os.environ.get('BOT_LANGUAGE', 'en'),
    }
    
    db_config = {
        'db_name': os.environ.get('DB_NAME'),
        'db_username': os.environ.get('DB_USERNAME'),
        'db_password': os.environ.get('DB_PASSWORD')
    }
    
    openai_helper = OpenAIHelper(config=openai_config)
    database = Database(config=db_config)
    telegram_bot = TelegramBot(config=telegram_config, openai=openai_helper, db=database)
    telegram_bot.run()