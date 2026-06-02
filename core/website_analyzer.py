
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

        try:

            async with session.get(
                website,
                timeout=10
            ) as response:

                html = await response.text()

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

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

                for a in soup.find_all(
                    "a",
                    href=True
                ):

                    href = a["href"]

                    if (
                        "instagram.com" in href and
                        not result["instagram"]
                    ):
                        result["instagram"] = href

                    elif (
                        "facebook.com" in href and
                        not result["facebook"]
                    ):
                        result["facebook"] = href

                    elif (
                        "linkedin.com" in href and
                        not result["linkedin"]
                    ):
                        result["linkedin"] = href

                    elif (
                        "youtube.com" in href and
                        not result["youtube"]
                    ):
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

        except Exception:

            result["website_broken"] = True

        business.update(result)

        return business

    # =====================================================
    # ANALYZE BATCH
    # =====================================================

    async def analyze_batch(
        self,
        businesses
    ):

        connector = aiohttp.TCPConnector(
            ssl=False
        )

        timeout = aiohttp.ClientTimeout(
            total=15
        )

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0"
                )
            }
        ) as session:

            tasks = [
                self.analyze(
                    session,
                    business
                )
                for business in businesses
            ]

            return await asyncio.gather(*tasks)

