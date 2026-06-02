
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class GoogleMapsConfig:
    api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")

    text_search_url: str = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
    )

    details_url: str = (
        "https://maps.googleapis.com/maps/api/place/details/json"
    )

    max_concurrent_requests: int = 10

    request_timeout: int = 15

    retry_attempts: int = 3

    retry_delay: int = 2

    # Only request minimal fields to reduce API cost
    detail_fields: list = field(default_factory=lambda: [
        "name",
        "formatted_address",
        "formatted_phone_number",
        "website",
        "rating",
        "user_ratings_total",
        "business_status"
    ])


@dataclass
class BusinessFilterConfig:

    # Main targeting
    target_category: str = "salon"
    target_city: str = "Bhubaneswar"

    # Lead qualification
    minimum_reviews: int = 30
    minimum_rating: float = 4.2

    # Prioritize businesses likely to buy
    prioritize_no_website: bool = True
    prioritize_facebook_only: bool = True
    prioritize_no_whatsapp: bool = True

    # Ignore weak businesses
    ignore_temporarily_closed: bool = True

    # Optional niche filtering
    allowed_categories: list = field(default_factory=lambda: [
        "salon",
        "spa",
        "gym",
        "restaurant",
        "dentist",
        "clinic",
        "cafe",
        "real estate agency"
    ])


@dataclass
class WebsiteAnalysisConfig:

    enabled: bool = True

    analyze_contact_page: bool = False

    detect_whatsapp: bool = True

    detect_booking_system: bool = True

    detect_social_links: bool = True

    detect_ssl: bool = True

    detect_platform: bool = True

    detect_outdated_site: bool = True

    max_page_size_mb: int = 2

    website_timeout: int = 10


@dataclass
class LeadScoringConfig:

    no_website_score: int = 45

    facebook_only_score: int = 20

    no_whatsapp_score: int = 15

    high_reviews_score: int = 15

    high_rating_score: int = 10

    outdated_website_score: int = 15

    broken_website_score: int = 25

    no_booking_score: int = 10

    weak_social_presence_score: int = 10

    max_score: int = 100


@dataclass
class ExportConfig:

    export_excel: bool = True

    export_csv: bool = True

    export_json: bool = True

    output_directory: str = "output"

    include_timestamp: bool = True


@dataclass
class LoggingConfig:

    log_level: str = "INFO"

    log_to_file: bool = True

    log_file: str = "lead_engine.log"


@dataclass
class AppConfig:

    google_maps: GoogleMapsConfig = field(
        default_factory=GoogleMapsConfig
    )

    business_filters: BusinessFilterConfig = field(
        default_factory=BusinessFilterConfig
    )

    website_analysis: WebsiteAnalysisConfig = field(
        default_factory=WebsiteAnalysisConfig
    )

    lead_scoring: LeadScoringConfig = field(
        default_factory=LeadScoringConfig
    )

    export: ExportConfig = field(
        default_factory=ExportConfig
    )

    logging: LoggingConfig = field(
        default_factory=LoggingConfig
    )


config = AppConfig()
