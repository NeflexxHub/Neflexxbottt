# FunPay Cardinal — Stars/Premium automation (example scaffold)

This repository is a **starter scaffold** for automating Telegram Stars/Premium delivery integrated with FunPay Cardinal.

**Important:** This project is a template. Replace placeholders (API keys, endpoints) with real, authorized credentials. Do **not** attempt to bypass service limits — use legitimate channels and follow provider rules.

## What's included
- `config.py` — configurable settings (API keys go here as environment variables).
- `models.py` — SQLAlchemy models using SQLite for quick testing.
- `fragment_adapter.py` — safe adapter with rate limiting and retry (uses tenacity).
- `funpay_adapter.py` — stub for FunPay integration (fill with your own API calls).
- `worker.py` — async worker that processes orders from a queue and uses an inventory pool.
- `bot.py` — aiogram-based Telegram handlers for `/create_lot`, `/myorders`, `/lastorders`.
- `main.py` — entry point to run the bot + worker together (development use).

## How to run (dev)
1. Create a virtualenv and install requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set environment variables (example):
```bash
export TG_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export FRAGMENT_API_KEY="your_fragment_api_key"
```

3. Run:
```bash
python main.py
```

## Notes & safety
- This scaffold uses SQLite for convenience. For production, switch to PostgreSQL and a proper message queue (Redis/RabbitMQ).
- The `fragment_adapter` contains a rate-limiter and retry logic — **do not** attempt to circumvent limits.
- Make sure all payment/provider accounts are KYC'd and abide by terms of service.
