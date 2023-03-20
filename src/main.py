import os
import dotenv
import logging
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from src.components import start, chat, home, commands
from src.db.base import engine, Base
from utils.filter import FilterButton
import openai


dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)
OPENAI_TOKEN = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_TOKEN


logging.basicConfig(
    filename='logs.log' if not DEBUG else None,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if DEBUG else logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(os.environ.get('BOT_TOKEN')).build()
    Base.metadata.create_all(engine)

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start.start)
        ],
        states={
            "SELECT_LANGUAGE": [
                CallbackQueryHandler(start.save_language, pattern='uz|ru|en')
            ],
            "CHAT": [
                MessageHandler(FilterButton('back'), home.display),
                MessageHandler(filters.TEXT, chat.complete)
            ],
            "HOME": [
                MessageHandler(FilterButton('start_chat'), chat.initialize),
                MessageHandler(FilterButton('essay_help'), home.coming_soon),
                MessageHandler(FilterButton('code_help'), home.coming_soon),
                MessageHandler(FilterButton('my_account'), home.coming_soon),
                MessageHandler(FilterButton('support'), home.coming_soon)
            ]
        },
        fallbacks=[
            CommandHandler('start', start.start),
            CommandHandler('help', commands.help)
        ]
    )

    application.add_handler(main_conversation)

    application.run_polling()
