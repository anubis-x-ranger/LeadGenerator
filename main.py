
import asyncio
from core.maps_client import GoogleMapsClient
from core.scorer import LeadScorer
from core.exporter import Exporter
from core.website_analyzer import WebsiteAnalyzer
from core.filters import LeadFilter

TARGET_CATEGORY = "gyms"
TARGET_CITY = "Mumbai"
SUB_AREAS = [
        "Andheri", "Bandra", "Powai",
        "Borivali", "Thane", "Dadar",
        "Juhu", "Malad", "Goregaon"
    ]
async def main():

    maps = GoogleMapsClient()
    analyzer = WebsiteAnalyzer()
    scorer = LeadScorer()

    businesses = await maps.search_businesses(
        category=TARGET_CATEGORY,
        city=TARGET_CITY,
        limit=200,
        sub_areas=SUB_AREAS
    )

    filtered = LeadFilter.filter_businesses(
        businesses,
        min_reviews=30,
        min_rating=4.2
    )

    detailed = await maps.fetch_details_batch(filtered)

    analyzed = await analyzer.analyze_batch(detailed)

    scored = scorer.score_batch(analyzed)

    Exporter.export_all(scored, f"{TARGET_CATEGORY}_{TARGET_CITY}")

if __name__ == "__main__":
    asyncio.run(main())
