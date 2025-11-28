from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.filters import Command
import asyncio
from models import init_db, Order, User
from sqlalchemy.orm import sessionmaker

Session = init_db()

bot = Bot(token=None)
dp = Dispatcher()

async def setup_bot(token):
    bot.session = bot.session if hasattr(bot, 'session') else None
    bot.token = token
    return Bot(token=token)

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    session = Session()
    user = session.query(User).filter(User.tg_id==message.from_user.id).first()
    if not user:
        user = User(tg_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
    await message.reply('Привет! Я бот для управления продажей Stars/Premium.')
    session.close()

@dp.message(Command('create_lot'))
async def cmd_create_lot(message: types.Message):
    # Expected: /create_lot <type> <amount> <price>
    parts = message.text.split()
    if len(parts) < 4:
        await message.reply('Использование: /create_lot stars 100 600')
        return
    _, typ, amount, price = parts[:4]
    # For demo we just acknowledge; in production call FunPayAdapter.create_lot
    await message.reply(f'Создаю лот: {typ} amount={amount} price={price}')

@dp.message(Command('myorders'))
async def cmd_myorders(message: types.Message):
    session = Session()
    orders = session.query(Order).filter(Order.buyer_tg_id==message.from_user.id).order_by(Order.created_at.desc()).limit(10).all()
    if not orders:
        await message.reply('У вас нет последних заказов')
        session.close()
        return
    lines = []
    for o in orders:
        lines.append(f'#{o.id} {o.amount} stars — {o.status} — {o.created_at}')
    await message.reply('\n'.join(lines))
    session.close()

@dp.message(Command('lastorders'))
async def cmd_lastorders(message: types.Message):
    # public last orders
    session = Session()
    orders = session.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    lines = []
    for o in orders:
        lines.append(f'#{o.id} {o.amount} stars — {o.status} — buyer:{o.buyer_tg_id}')
    await message.reply('\n'.join(lines))
    session.close()
