from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.text import button, text
import openai


async def initialize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data['language_code']
    await update.effective_message.reply_text("Nice! Start chatting with me!",
                                              reply_markup=ReplyKeyboardMarkup(
        [
            [button('back', language)]
        ], resize_keyboard=True
    ))
    
    return "CHAT"

async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.effective_message.text
    
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{text}"}
            ]
        )
    
    await context.bot.send_chat_action(chat_id, action='TYPING')
    await update.effective_message.reply_text(response['choices'][0]['message']['content'])