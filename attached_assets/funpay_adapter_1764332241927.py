import aiohttp
from config import FUNPAY_API_KEY

class FunPayAdapter:
    def __init__(self, api_key=FUNPAY_API_KEY, session=None):
        self.api_key = api_key
        self.session = session or aiohttp.ClientSession()

    async def create_lot(self, title: str, price: float, count: int):
        # Implement FunPay API call to create a lot. This is a stub.
        # Use proper endpoints, authentication and error handling.
        return {"ok": True, "lot_id": "stub_lot_123"}

    async def get_orders(self):
        # Poll or receive webhooks from FunPay; stub for demo
        return []
