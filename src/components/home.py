from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.text import text, button


async def display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    language = context.user_data['language_code']
    
    buttons = [
        [KeyboardButton(button('start_chat', language))]
    ]
    
    await update.effective_message.reply_text(text('home', language),
                                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                              parse_mode='HTML')
    
    return "HOME"