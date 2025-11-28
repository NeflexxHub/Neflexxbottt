import asyncio
from models import init_db, Order, Inventory, OrderEvent
from fragment_adapter import FragmentAdapter
from sqlalchemy.orm import sessionmaker
from config import WORKER_CONCURRENCY
import datetime

Session = init_db()

class Worker:
    def __init__(self, concurrency=WORKER_CONCURRENCY):
        self.queue = asyncio.Queue()
        self.fragment = FragmentAdapter()
        self.concurrency = concurrency
        self._workers = []

    async def start(self):
        for _ in range(self.concurrency):
            w = asyncio.create_task(self._worker())
            self._workers.append(w)

    async def stop(self):
        for _ in self._workers:
            await self.queue.put(None)
        await asyncio.gather(*self._workers)

    async def enqueue_order(self, order_id: int):
        await self.queue.put(order_id)

    async def _worker(self):
        while True:
            order_id = await self.queue.get()
            if order_id is None:
                break
            try:
                await self.process(order_id)
            except Exception as e:
                print('Worker error:', e)
            finally:
                self.queue.task_done()

    async def process(self, order_id: int):
        session = Session()
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            session.close()
            return
        if order.status != 'new':
            session.close()
            return
        # Reserve an inventory entry atomically (simplified)
        inv = session.query(Inventory).filter(Inventory.status=='available', Inventory.type=='stars').first()
        if not inv:
            order.status = 'waiting_for_inventory'
            session.add(order)
            session.commit()
            session.close()
            return
        inv.status = 'reserved'
        inv.reserved_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        session.add(inv)
        order.status = 'processing'
        session.add(order)
        session.commit()

        # Attempt issuance via Fragment
        try:
            print(f'Issuing {order.amount} stars to {order.buyer_tg_id} using provider ref {inv.provider_ref}')
            resp = await self.fragment.buy_stars(order.amount, int(order.buyer_tg_id))
            # mark inventory used
            inv.status = 'used'
            order.status = 'done'
            session.add(inv)
            session.add(order)
            session.commit()
            # log event
            ev = OrderEvent(order_id=order.id, event_type='issued', payload=resp)
            session.add(ev)
            session.commit()
        except Exception as exc:
            print('Issuance failed:', exc)
            inv.status = 'available'
            order.status = 'failed'
            session.add(inv)
            session.add(order)
            session.commit()
        finally:
            session.close()
