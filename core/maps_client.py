
import aiohttp
import asyncio
import os

BASE_URL = "https://maps.googleapis.com/maps/api"

class GoogleMapsClient:

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.semaphore = asyncio.Semaphore(10)

    async def search_businesses(self, category, city,limit=10):

        query = f"{category} in {city}"

        url = f"{BASE_URL}/place/textsearch/json"

        params = {
            "query": query,
            "key": self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
        results = data.get("results", [])[:limit]
        return results

    async def fetch_place_details(self, session, place_id):

        async with self.semaphore:

            url = f"{BASE_URL}/place/details/json"

            fields = ",".join([
                "name",
                "website",
                "formatted_phone_number",
                "formatted_address",
                "rating",
                "user_ratings_total"
            ])

            params = {
                "place_id": place_id,
                "fields": fields,
                "key": self.api_key
            }

            async with session.get(url, params=params) as response:
                data = await response.json()

                return data.get("result", {})

    async def fetch_details_batch(self, businesses):

        async with aiohttp.ClientSession() as session:

            tasks = [
                self.fetch_place_details(
                    session,
                    business["place_id"]
                )
                for business in businesses
            ]

            return await asyncio.gather(*tasks)

