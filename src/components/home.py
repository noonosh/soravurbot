from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from utils.text import text, button
from utils.language import lang


async def display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    language = lang(chat_id, context)
    
    buttons = [
        [
            KeyboardButton(button('start_chat', language))
        ],
        [
            KeyboardButton(button('essay_help', language)),
            KeyboardButton(button('code_help', language))
        ],
        [
            KeyboardButton(button('my_account', language)),
            KeyboardButton(button('support', language))
        ]
    ]
    
    await update.effective_message.reply_text(text('home', language),
                                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                              parse_mode='HTML')
    
    return "HOME"


async def coming_soon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text('<b>🤭 Coming soon</b>', parse_mode='HTML')