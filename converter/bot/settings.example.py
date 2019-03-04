import logging

TELEGRAM_API_TOKEN = ''

ADMINS = ['@USERNAME']

# More information about polling and webhooks can be found here:
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
MODE = {
    'active': 'polling',  # "webook" or "polling"
    # 'configuration': {
    #     'listen': '127.0.0.1',
    #     'port': 5000,
    #     'url_path': TELEGRAM_API_TOKEN,
    #     'url': 'https://your_domain.tld/%s' % TELEGRAM_API_TOKEN,
    # },
}

LOG_LEVEL = logging.DEBUG
