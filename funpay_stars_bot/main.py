import asyncio
import os
from bot import dp, bot, setup_bot
from worker import Worker
from config import TG_BOT_TOKEN
from models import init_db

async def main():
    # Initialize DB
    init_db()

    # setup bot
    telegram_bot = await setup_bot(TG_BOT_TOKEN)

    # start worker
    worker = Worker()
    await worker.start()

    # For demo purposes we won't start aiogram long-polling in this scaffold (user can run with their own runner)
    print('Scaffold started. Start polling with aiogram from your environment, or integrate into your runloop.')

    # Keep alive
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print('Shutting down...')
        await worker.stop()

if __name__ == '__main__':
    asyncio.run(main())
