import logging
import time
from base64 import b64decode
from io import BytesIO

import requests
from telegram import Bot, Update
from telegram.ext import MessageHandler, run_async
from telegram.ext.filters import Filters
from telegram.parsemode import ParseMode

from converter.bot import settings
from converter.bot.bot import converter_bot


class Command:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        converter_bot.add_command(handler=MessageHandler, func=self.convert_message_handler, filters=Filters.all)

    # # # # # # # # #
    # USER COMMANDS #
    # # # # # # # # #

    @run_async
    def convert_message_handler(self, bot: Bot, update: Update):
        data = {
            'apikey': settings.CONVERTIO_API_KEY,
        }
        attachment = update.message.effective_attachment
        file = bot.get_file(attachment.file_id)
        filename, extension = file.file_path.rstrip('/').rsplit('/', 1)[1].rsplit('.', 1)
        data['file'] = file.file_path

        if extension in ['webm', 'mov', 'mkv', 'gif']:
            output_format = 'mp4'
            filename += f'.mp4'
        elif extension in ['mp4']:
            output_format = 'gif'
            filename += f'.gif.remove_this'

        data['outputformat'] = output_format

        if not output_format :
            update.message.reply_text('This file format is currently not supported')
            return

        original_text = f'Converting from `{extension}` to `{output_format}`\n'
        sent_message = update.message.reply_text(original_text,
                                                 parse_mode=ParseMode.MARKDOWN,
                                                 reply_to_message_id=update.message.message_id).result()
        try:
            conversion = requests.post('https://api.convertio.co/convert', json=data)
            conversion.raise_for_status()

            conversion_id = conversion.json()['data']['id']
            status = {}
            counter = 0
            while status.get('data', {}).get('step') != 'finish':
                time.sleep(1)
                status_response = requests.get(f'https://api.convertio.co/convert/{conversion_id}/status', json={})
                status_response.raise_for_status()
                status = status_response.json()
                counter += 1

                sent_message.edit_text(original_text + ('.' * counter), parse_mode=ParseMode.MARKDOWN)

            file_response = requests.get(f'https://api.convertio.co/convert/{conversion_id}/dl/', json={})
            file_response.raise_for_status()
            file = file_response.json()
            sent_message.edit_text(original_text + 'Finished', parse_mode=ParseMode.MARKDOWN)
            bot.send_document(chat_id=update.message.chat.id,
                              caption='Due to TG converting `gifs` to `mp4` I added a suffix, which is to be removed'
                                if output_format == 'gif' else '',
                              document=BytesIO(b64decode(file['data']['content'])),
                              filename=filename,
                              reply_to_message_id=update.message.message_id,
                              parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            update.message.reply_text('An error occurred somewhere while converting.',
                                      reply_message_id=update.message.message_id)
            raise e


command = Command()
