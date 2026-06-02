from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict


# =========================================================
# WEBSITE ANALYSIS MODEL
# =========================================================

@dataclass
class WebsiteAnalysis:

    has_ssl: bool = False

    has_whatsapp: bool = False

    booking_detected: bool = False

    website_broken: bool = False

    outdated_website: bool = False

    facebook_only: bool = False

    cms: str = ""

    website_title: str = ""

    emails: List[str] = field(default_factory=list)

    instagram: str = ""

    facebook: str = ""

    linkedin: str = ""

    youtube: str = ""

    social_count: int = 0


# =========================================================
# LEAD SCORING MODEL
# =========================================================

@dataclass
class LeadScore:

    lead_score: int = 0

    opportunity: str = "LOW"

    primary_offer: str = ""

    score_reasons: List[str] = field(default_factory=list)

    recommended_services: List[str] = field(default_factory=list)


# =========================================================
# MAIN BUSINESS LEAD MODEL
# =========================================================

@dataclass
class BusinessLead:

    # -----------------------------------------------------
    # GOOGLE MAPS DATA
    # -----------------------------------------------------

    place_id: str = ""

    name: str = ""

    category: str = ""

    address: str = ""

    city: str = ""

    phone: str = ""

    website: str = ""

    rating: float = 0.0

    review_count: int = 0

    business_status: str = ""

    google_maps_url: str = ""

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    # -----------------------------------------------------
    # QUALIFICATION FLAGS
    # -----------------------------------------------------

    no_website: bool = False

    high_review_business: bool = False

    qualified: bool = False

    # -----------------------------------------------------
    # WEBSITE ANALYSIS
    # -----------------------------------------------------

    website_analysis: WebsiteAnalysis = field(
        default_factory=WebsiteAnalysis
    )

    # -----------------------------------------------------
    # LEAD SCORING
    # -----------------------------------------------------

    lead_score: LeadScore = field(
        default_factory=LeadScore
    )

    # -----------------------------------------------------
    # SALES NOTES
    # -----------------------------------------------------

    notes: str = ""

    outreach_angle: str = ""

    # -----------------------------------------------------
    # SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self) -> Dict:

        data = asdict(self)

        # Flatten nested objects for export
        website_data = data.pop("website_analysis", {})
        score_data = data.pop("lead_score", {})

        data.update(website_data)
        data.update(score_data)

        return data


# =========================================================
# SCRAPE RESULT MODEL
# =========================================================

@dataclass
class ScrapeResult:

    total_found: int = 0

    total_qualified: int = 0

    total_high_opportunity: int = 0

    leads: List[BusinessLead] = field(default_factory=list)

    execution_time_seconds: float = 0.0

    api_requests_used: int = 0

    estimated_api_cost: float = 0.0

