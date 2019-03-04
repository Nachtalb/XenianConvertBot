import logging
from datetime import timedelta
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import run_async, MessageHandler
from telegram.ext.filters import Filters
from telegram.parsemode import ParseMode


from converter.bot.bot import converter_bot
from converter.bot import settings


class Command:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        converter_bot.add_command(handler=MessageHandler, func=self.convert_message_handler, filters=Filters.all)

    # # # # # # # # #
    # USER COMMANDS #
    # # # # # # # # #

    @run_async
    def convert_message_handler(self, bot: Bot, update: Update):
        update.message.reply_text('Recieved a message')

command = Command()
