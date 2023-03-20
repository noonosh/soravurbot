from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from utils.text import button, text
from utils.language import lang
import openai
import time


async def initialize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    language = lang(chat_id, context)
    await update.effective_message.reply_text(text('chat', language),
                                              reply_markup=ReplyKeyboardMarkup(
        [
            [button('back', language)]
        ], resize_keyboard=True
    ), parse_mode='HTML')
    
    return "CHAT"

async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.effective_message.text
    
    language = lang(chat_id, context)
    
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    
    try:
        
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{text}"}
                ]
            )
        
        completion = response['choices'][0]['message']['content']    
    
    except Exception as e:
        completion = text('error', language)
    
    time.sleep(0.5)
    await update.effective_message.reply_text(completion, parse_mode='HTML')
    