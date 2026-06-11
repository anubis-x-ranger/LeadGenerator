import aiohttp
import asyncio
import os

BASE_URL = "https://maps.googleapis.com/maps/api"


class GoogleMapsClient:

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.semaphore = asyncio.Semaphore(10)

    async def search_businesses(
        self,
        category: str,
        city: str,
        limit: int = 200,
        sub_areas: list = None
    ) -> list:

        queries = []

        if sub_areas:
            for area in sub_areas:
                queries.append(f"{category} in {area} {city}")
        else:
            queries.append(f"{category} in {city}")

        seen_ids = set()
        all_results = []

        # Sequential — NOT concurrent. Running paginated queries in
        # parallel causes next_page_tokens to collide and fail on
        # Google's backend, producing INVALID_REQUEST on every page 2.
        async with aiohttp.ClientSession() as session:
            for query in queries:
                if len(all_results) >= limit:
                    break

                print(f"\n[>] Searching: {query}")

                results = await self._paginate_query(
                    session, query, limit - len(all_results)
                )

                for r in results:
                    pid = r.get("place_id")
                    if pid and pid not in seen_ids:
                        seen_ids.add(pid)
                        all_results.append(r)

        print(f"\n[✓] Total unique results collected: {len(all_results)}")
        return all_results[:limit]

    async def _paginate_query(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int
    ) -> list:

        url = f"{BASE_URL}/place/textsearch/json"
        results = []
        next_page_token = None

        for page in range(3):  # Google caps at 3 pages = 60 results max
            if len(results) >= limit:
                break

            if next_page_token:
                params = {
                    "pagetoken": next_page_token,
                    "key": self.api_key
                }
            else:
                params = {
                    "query": query,
                    "key": self.api_key
                }

            # Retry loop for next_page_token — Google needs time to
            # activate the token server-side. INVALID_REQUEST here means
            # "not ready yet", not a permanent error. Retry with backoff.
            for attempt in range(5):
                async with session.get(url, params=params) as response:
                    data = await response.json()

                status = data.get("status")

                if status == "OK":
                    break

                if status == "ZERO_RESULTS":
                    return results

                if status == "INVALID_REQUEST" and next_page_token:
                    wait = 2 + (attempt * 2)  # 2s, 4s, 6s, 8s, 10s
                    print(f"    [~] Token not ready (attempt {attempt + 1}), retrying in {wait}s...")
                    await asyncio.sleep(wait)
                    continue

                # Any other error (OVER_QUERY_LIMIT, REQUEST_DENIED etc.)
                print(f"    [!] API error on page {page + 1}: {status}")
                return results

            else:
                # All retries exhausted
                print(f"    [!] Token failed after all retries — skipping page {page + 1}")
                return results

            page_results = data.get("results", [])
            results.extend(page_results)
            print(f"    [+] Page {page + 1}: {len(page_results)} results")

            next_page_token = data.get("next_page_token")

            if not next_page_token:
                break

            # Initial delay before fetching next page
            await asyncio.sleep(3)

        return results[:limit]

    async def fetch_place_details(self, session, business: dict) -> dict:

        async with self.semaphore:

            place_id = business.get("place_id")
            if not place_id:
                return business

            url = f"{BASE_URL}/place/details/json"

            fields = ",".join([
                "name",
                "website",
                "formatted_phone_number",
                "formatted_address",
                "rating",
                "user_ratings_total",
                "business_status"
            ])

            params = {
                "place_id": place_id,
                "fields": fields,
                "key": self.api_key
            }

            try:
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    detail = data.get("result", {})

                # Merge: keep original fields, overlay with fresh details
                return {**business, **detail}

            except Exception as e:
                print(f"    [!] Detail fetch failed for {place_id}: {e}")
                return business

    async def fetch_details_batch(self, businesses: list) -> list:

        async with aiohttp.ClientSession() as session:

            tasks = [
                self.fetch_place_details(session, business)
                for business in businesses
            ]

            return await asyncio.gather(*tasks)