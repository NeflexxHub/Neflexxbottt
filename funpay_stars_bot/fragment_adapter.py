import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential
from config import FRAGMENT_API_KEY, FRAGMENT_BASE_URL

# Local concurrency limit to avoid hitting provider too hard
SEM = asyncio.Semaphore(3)

class FragmentAdapter:
    def __init__(self, api_key=FRAGMENT_API_KEY, base_url=FRAGMENT_BASE_URL, session=None):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = session or aiohttp.ClientSession()

    async def _headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=10))
    async def buy_stars(self, amount: int, target_tg_id: int):
        """Ask provider to buy/send stars to target_tg_id.
        This is a stub — replace endpoint and payload to match your provider's API.
        The retry decorator will attempt on transient errors.
        """
        payload = {"amount": amount, "tg_id": target_tg_id}
        async with SEM:
            async with self.session.post(f"{self.base_url}/stars/buy", json=payload, headers=await self._headers(), timeout=30) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    # Raise to trigger retry for transient errors like 429/5xx
                    raise Exception(f"Fragment error {resp.status}: {text}")
                return await resp.json()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=10))
    async def buy_premium(self, sku: str, target_tg_id: int):
        payload = {"sku": sku, "tg_id": target_tg_id}
        async with SEM:
            async with self.session.post(f"{self.base_url}/premium/buy", json=payload, headers=await self._headers(), timeout=30) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    raise Exception(f"Fragment error {resp.status}: {text}")
                return await resp.json()
