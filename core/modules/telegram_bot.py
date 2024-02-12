from __future__ import annotations

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes, \
	ApplicationBuilder, CommandHandler, MessageHandler, \
	ConversationHandler, filters, InlineQueryHandler, CallbackQueryHandler

from core.modules.utils import error_handler
from core.modules.openai_helper import OpenAIHelper


class TelegramBot:
	
	def __init__(self, config: dict, openai: OpenAIHelper):
		self.config = config
		self.openai = openai
	
	
	async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		await update.effective_message.reply_text(
			f'Bot set up. Config details:\n\n<code>{self.config}</code>\n\n<code>{self.openai}</code>',
			parse_mode="HTML")
	
	def run(self):
		application = ApplicationBuilder() \
			.token(self.config['token']) \
			.concurrent_updates(True) \
			.build()

		application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))

		application.add_error_handler(error_handler)

		application.run_polling()