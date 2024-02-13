from __future__ import annotations

import logging
import asyncio

from telegram import Update, constants
from telegram.error import RetryAfter, TimedOut, BadRequest
from telegram.ext import CallbackContext, ContextTypes, \
	ApplicationBuilder, CommandHandler, MessageHandler, \
	ConversationHandler, filters, InlineQueryHandler, CallbackQueryHandler

from core.utils import add_chat_request_to_usage_tracker, edit_message_with_retry, get_reply_to_message_id, handle_direct_result, is_direct_result, error_handler, generate_available_locale_buttons, message_text, \
	is_group_chat, is_user_in_group, get_thread_id, get_stream_cutoff_values, split_into_chunks, wrap_with_indicator, localized_text, translations
from core.modules.openai_helper import OpenAIHelper
from core.db.db import Database


class TelegramBot:
	
	def __init__(self, config: dict, openai: OpenAIHelper, db: Database):
		self.config = config
		self.openai = openai
		self.db = db
		self.user = {}
		self.usage = {}
		self.last_message = {}
		
	async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		uid = update.message.from_user.id
		full_name = str(update.effective_chat.first_name) + ' ' + str(update.effective_chat.last_name)
		
		
		if uid not in self.user.keys():
			self.user[uid] = {
				'name': full_name
			}
			logging.info(self.user)
			return await update.effective_message.reply_text(
				"\n".join(translations['available_locale'][i]['prompt'] for i in translations['available_locale'].keys()),
				reply_markup=generate_available_locale_buttons(),
				parse_mode=constants.ParseMode.HTML)
		await update.effective_message.reply_text(localized_text(
			'general_description', self.user[uid]['language']
			))
		
	async def get_user_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
		try:
			query = update.callback_query
			data = query.data
			await query.answer()
			uid = update.effective_chat.id
			
			if data in [i for i in translations.keys()]:
				self.user[uid]['language'] = data
			
			language_code = self.user[uid]['language']
			
			await update.callback_query.delete_message()
			
			await update.effective_message.reply_text(localized_text('general_description', language_code))
		except Exception as e:
			logging.exception("Exception: ", e)
	
	
	async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
			"""
			React to incoming messages and respond accordingly.
			"""
			if update.edited_message or not update.message or update.message.via_bot:
				return

			logging.info(
				f'New message received from user {update.message.from_user.name} (id: {update.message.from_user.id})')
			chat_id = update.effective_chat.id
			user_id = update.message.from_user.id
			prompt = message_text(update.message)
			self.last_message[chat_id] = prompt

			if is_group_chat(update):
				return
				# trigger_keyword = self.config['group_trigger_keyword']

				# if prompt.lower().startswith(trigger_keyword.lower()) or update.message.text.lower().startswith('/chat'):
				# 	if prompt.lower().startswith(trigger_keyword.lower()):
				# 		prompt = prompt[len(trigger_keyword):].strip()

				# 	if update.message.reply_to_message and \
				# 			update.message.reply_to_message.text and \
				# 			update.message.reply_to_message.from_user.id != context.bot.id:
				# 		prompt = f'"{update.message.reply_to_message.text}" {prompt}'
				# else:
				# 	if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
				# 		logging.info('Message is a reply to the bot, allowing...')
				# 	else:
				# 		logging.warning('Message does not start with trigger keyword, ignoring...')
				# 		return

			try:
				total_tokens = 0

				await update.effective_message.reply_chat_action(
					action=constants.ChatAction.TYPING,
					message_thread_id=get_thread_id(update)
				)

				stream_response = self.openai.get_chat_response_stream(chat_id=chat_id, query=prompt)
				i = 0
				prev = ''
				sent_message = None
				backoff = 0
				stream_chunk = 0

				async for content, tokens in stream_response:
					if is_direct_result(content):
						return await handle_direct_result(self.config, update, content)

					if len(content.strip()) == 0:
						continue

					stream_chunks = split_into_chunks(content)
					if len(stream_chunks) > 1:
						content = stream_chunks[-1]
						if stream_chunk != len(stream_chunks) - 1:
							stream_chunk += 1
							try:
								await edit_message_with_retry(context, chat_id, str(sent_message.message_id),
															stream_chunks[-2])
							except:
								pass
							try:
								sent_message = await update.effective_message.reply_text(
									message_thread_id=get_thread_id(update),
									text=content if len(content) > 0 else "..."
								)
							except:
								pass
							continue

					cutoff = get_stream_cutoff_values(update, content)
					cutoff += backoff

					if i == 0:
						try:
							if sent_message is not None:
								await context.bot.delete_message(chat_id=sent_message.chat_id,
																message_id=sent_message.message_id)
							sent_message = await update.effective_message.reply_text(
								message_thread_id=get_thread_id(update),
								reply_to_message_id=get_reply_to_message_id(self.config, update),
								text=content,
							)
						except:
							continue

					elif abs(len(content) - len(prev)) > cutoff or tokens != 'not_finished':
						prev = content

						try:
							use_markdown = tokens != 'not_finished'
							await edit_message_with_retry(context, chat_id, str(sent_message.message_id),
														text=content, markdown=use_markdown)

						except RetryAfter as e:
							backoff += 5
							await asyncio.sleep(e.retry_after)
							continue

						except TimedOut:
							backoff += 5
							await asyncio.sleep(0.5)
							continue

						except Exception:
							backoff += 5
							continue

						await asyncio.sleep(0.01)

					i += 1
					if tokens != 'not_finished':
						total_tokens = int(tokens)


			except Exception as e:
				logging.exception(e)
				await update.effective_message.reply_text(
					message_thread_id=get_thread_id(update),
					reply_to_message_id=get_reply_to_message_id(self.config, update),
					text=f"{localized_text('chat_fail', self.config['bot_language'])} {str(e)}",
					parse_mode=constants.ParseMode.MARKDOWN
				)
		
	async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
			"""
			Shows the help menu.
			"""
			u = update.effective_chat.id
			help_text = localized_text('help_menu', self.user[u]['language'])
			await update.message.reply_text(help_text, disable_web_page_preview=True)
	
	def run(self):
		application = ApplicationBuilder() \
			.token(self.config['token']) \
			.build()
		
		application.add_handler(CommandHandler('start', self.start))
		application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))
		application.add_handler(CallbackQueryHandler(self.get_user_language))
		application.add_error_handler(error_handler)

		application.run_polling()