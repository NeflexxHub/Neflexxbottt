import os

# Telegram
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', 'REPLACE_WITH_TOKEN')

# Fragment / provider
FRAGMENT_API_KEY = os.getenv('FRAGMENT_API_KEY', 'REPLACE_WITH_KEY')
FRAGMENT_BASE_URL = os.getenv('FRAGMENT_BASE_URL', 'https://api.fragment.example')

# FunPay
FUNPAY_API_KEY = os.getenv('FUNPAY_API_KEY', 'REPLACE_FUNPAY_KEY')

# Worker / concurrency
WORKER_CONCURRENCY = int(os.getenv('WORKER_CONCURRENCY', '10'))
