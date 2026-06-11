import aiohttp
import asyncio
from bs4 import BeautifulSoup


class WebsiteAnalyzer:

    async def analyze(
        self,
        session,
        business
    ):

        website = business.get("website")

        if not website:
            business["no_website"] = True
            return business

        result = {
            "has_ssl": website.startswith("https"),
            "has_whatsapp": False,
            "booking_detected": False,
            "website_broken": False,
            "outdated_website": False,
            "cms": "",
            "instagram": "",
            "facebook": "",
            "linkedin": "",
            "youtube": ""
        }

        # aiohttp requires a ClientTimeout object — a plain int crashes
        per_site_timeout = aiohttp.ClientTimeout(total=10)

        try:

            async with session.get(
                website,
                timeout=per_site_timeout,
                allow_redirects=True
            ) as response:

                # Only read up to 2MB to avoid hanging on huge pages
                raw = await response.content.read(2 * 1024 * 1024)
                html = raw.decode("utf-8", errors="ignore")

                soup = BeautifulSoup(html, "html.parser")
                html_lower = html.lower()

                # ==========================================
                # WHATSAPP DETECTION
                # ==========================================

                result["has_whatsapp"] = (
                    "wa.me" in html_lower or
                    "whatsapp" in html_lower
                )

                # ==========================================
                # BOOKING DETECTION
                # ==========================================

                result["booking_detected"] = (
                    "book now" in html_lower or
                    "appointment" in html_lower or
                    "schedule" in html_lower
                )

                # ==========================================
                # CMS DETECTION
                # ==========================================

                if "wp-content" in html_lower:
                    result["cms"] = "wordpress"
                elif "wix" in html_lower:
                    result["cms"] = "wix"
                elif "shopify" in html_lower:
                    result["cms"] = "shopify"

                # ==========================================
                # SOCIAL LINKS
                # ==========================================

                for a in soup.find_all("a", href=True):

                    href = a["href"]

                    if "instagram.com" in href and not result["instagram"]:
                        result["instagram"] = href

                    elif "facebook.com" in href and not result["facebook"]:
                        result["facebook"] = href

                    elif "linkedin.com" in href and not result["linkedin"]:
                        result["linkedin"] = href

                    elif "youtube.com" in href and not result["youtube"]:
                        result["youtube"] = href

                # ==========================================
                # OUTDATED SITE SIGNALS
                # ==========================================

                outdated_signals = [
                    "visitor counter",
                    "powered by blogger",
                    "frameset",
                    "table layout"
                ]

                result["outdated_website"] = any(
                    signal in html_lower
                    for signal in outdated_signals
                )

        except asyncio.TimeoutError:
            # Site took too long — treat as broken
            result["website_broken"] = True
            print(f"    [timeout] {website}")

        except Exception as e:
            # Any other network/parse error — mark broken, never crash batch
            result["website_broken"] = True
            print(f"    [error] {website} — {type(e).__name__}")

        business.update(result)
        return business

    # =====================================================
    # ANALYZE BATCH
    # =====================================================

    async def analyze_batch(self, businesses):

        connector = aiohttp.TCPConnector(
            limit=20,       # max open connections
            ssl=False
        )

        # Session-level timeout acts as a hard ceiling per request
        session_timeout = aiohttp.ClientTimeout(total=20)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=session_timeout,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        ) as session:

            tasks = [
                self.analyze(session, business)
                for business in businesses
            ]

            # return_exceptions=True means one bad site
            # never kills the rest of the batch
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Replace any uncaught exceptions with the original business dict
            cleaned = []
            for i, r in enumerate(results):
                if isinstance(r, Exception):
                    print(f"    [uncaught] {type(r).__name__}: {r}")
                    businesses[i]["website_broken"] = True
                    cleaned.append(businesses[i])
                else:
                    cleaned.append(r)

            return cleaned