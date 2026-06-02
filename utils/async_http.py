
import aiohttp
import asyncio
from utils.retry import async_retry


class AsyncHTTPClient:

    def __init__(
        self,
        timeout: int = 15,
        max_connections: int = 10
    ):

        self.timeout = aiohttp.ClientTimeout(
            total=timeout
        )

        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            ssl=False
        )

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

    @async_retry(retries=3, delay=2)
    async def get_json(
        self,
        url: str,
        params: dict = None
    ):

        async with aiohttp.ClientSession(
            timeout=self.timeout,
            connector=self.connector,
            headers=self.headers
        ) as session:

            async with session.get(
                url,
                params=params
            ) as response:

                response.raise_for_status()

                return await response.json()

    @async_retry(retries=3, delay=2)
    async def get_text(
        self,
        url: str
    ):

        async with aiohttp.ClientSession(
            timeout=self.timeout,
            connector=self.connector,
            headers=self.headers
        ) as session:

            async with session.get(url) as response:

                response.raise_for_status()

                return await response.text()

    async def close(self):
        pass

