from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from utils.text import text, button
from src.db.base import session
from src.db.models import User
from sqlalchemy import select
from src.components.home import display as home_display



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    session.add(
        User(
            user_id=chat_id,
            first_name=user.first_name,
            last_name=user.last_name
        )    
    )
    session.commit()
    session.close()

    markup = [
        [
            InlineKeyboardButton(button('language', 'en'), callback_data='en'),
            InlineKeyboardButton(button('language', 'ru'), callback_data='ru'),
            InlineKeyboardButton(button('language', 'uz'), callback_data='uz')
        ]
    ]
    await update.effective_message.reply_text(text('start', 'default'), reply_markup=ReplyKeyboardRemove())
    await update.effective_message.reply_text(text('choose_language', 'default'), reply_markup=InlineKeyboardMarkup(markup))
    
    return "SELECT_LANGUAGE"


async def save_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    
    user = session.query(User).filter(User.user_id == chat_id).scalar()
    user.language_code = query.data
    
    context.user_data.update(
        {
            "language_code": query.data
        }
    )
    
    session.commit()
    
    await update.effective_message.reply_text("Language saved")
    
    return await home_display(update, context)    
    