from telegram.ext.filters import MessageFilter
from utils.text import j


class FilterButton(MessageFilter):
    def __init__(self, key: str):
        self.key = key

    def filter(self, message):
        langs = j["buttons"][self.key]
        buttons = []
        for i in langs:
            buttons.append(langs[i])
        return message.text in buttons