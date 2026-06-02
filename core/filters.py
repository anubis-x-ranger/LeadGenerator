from typing import List
from config import config
from core.models import BusinessLead


class LeadFilter:

    @staticmethod
    def filter_businesses(
        businesses: List[dict],
        min_reviews: int = None,
        min_rating: float = None
    ) -> List[dict]:

        settings = config.business_filters

        min_reviews = (
            min_reviews
            if min_reviews is not None
            else settings.minimum_reviews
        )

        min_rating = (
            min_rating
            if min_rating is not None
            else settings.minimum_rating
        )

        filtered = []

        for business in businesses:

            reviews = business.get(
                "user_ratings_total",
                0
            )

            rating = business.get(
                "rating",
                0
            )

            business_status = business.get(
                "business_status",
                ""
            )

            # =====================================================
            # FILTER 1 — MINIMUM REVIEWS
            # =====================================================

            if reviews < min_reviews:
                continue

            # =====================================================
            # FILTER 2 — MINIMUM RATING
            # =====================================================

            if rating < min_rating:
                continue

            # =====================================================
            # FILTER 3 — BUSINESS STATUS
            # =====================================================

            if (
                settings.ignore_temporarily_closed and
                business_status == "CLOSED_TEMPORARILY"
            ):
                continue

            filtered.append(business)

        return filtered

    # =============================================================
    # PRIORITY SORTING
    # =============================================================

    @staticmethod
    def prioritize_leads(
        businesses: List[BusinessLead]
    ) -> List[BusinessLead]:

        def priority_score(business: BusinessLead):

            score = 0

            # -----------------------------------------------------
            # NO WEBSITE = VERY HIGH PRIORITY
            # -----------------------------------------------------

            if not business.website:
                score += 50

            # -----------------------------------------------------
            # HIGH REVIEW COUNT
            # -----------------------------------------------------

            if business.review_count >= 200:
                score += 25

            elif business.review_count >= 100:
                score += 15

            # -----------------------------------------------------
            # HIGH RATING
            # -----------------------------------------------------

            if business.rating >= 4.7:
                score += 15

            # -----------------------------------------------------
            # FACEBOOK ONLY
            # -----------------------------------------------------

            if (
                business.website_analysis.facebook and
                not business.website
            ):
                score += 20

            # -----------------------------------------------------
            # NO WHATSAPP
            # -----------------------------------------------------

            if (
                not business.website_analysis.has_whatsapp
            ):
                score += 10

            # -----------------------------------------------------
            # BROKEN WEBSITE
            # -----------------------------------------------------

            if (
                business.website_analysis.website_broken
            ):
                score += 25

            return score

        return sorted(
            businesses,
            key=priority_score,
            reverse=True
        )

    # =============================================================
    # FILTER ONLY HIGH OPPORTUNITY LEADS
    # =============================================================

    @staticmethod
    def high_opportunity_only(
        businesses: List[BusinessLead]
    ) -> List[BusinessLead]:

        return [
            business
            for business in businesses
            if business.lead_score.lead_score >= 70
        ]

    # =============================================================
    # FILTER BUSINESSES WITHOUT WEBSITES
    # =============================================================

    @staticmethod
    def no_website_only(
        businesses: List[BusinessLead]
    ) -> List[BusinessLead]:

        return [
            business
            for business in businesses
            if not business.website
        ]

    # =============================================================
    # FILTER FACEBOOK-ONLY BUSINESSES
    # =============================================================

    @staticmethod
    def facebook_only_businesses(
        businesses: List[BusinessLead]
    ) -> List[BusinessLead]:

        filtered = []

        for business in businesses:

            has_facebook = bool(
                business.website_analysis.facebook
            )

            has_website = bool(
                business.website
            )

            if has_facebook and not has_website:
                filtered.append(business)

        return filtered

    # =============================================================
    # FILTER WEAK DIGITAL PRESENCE
    # =============================================================

    @staticmethod
    def weak_digital_presence(
        businesses: List[BusinessLead]
    ) -> List[BusinessLead]:

        filtered = []

        for business in businesses:

            weak_presence = False

            analysis = business.website_analysis

            # No website
            if not business.website:
                weak_presence = True

            # Broken website
            elif analysis.website_broken:
                weak_presence = True

            # No WhatsApp
            elif not analysis.has_whatsapp:
                weak_presence = True

            # No booking
            elif not analysis.booking_detected:
                weak_presence = True

            # Weak social presence
            elif analysis.social_count <= 1:
                weak_presence = True

            if weak_presence:
                filtered.append(business)

        return filtered

    # =============================================================
    # NICHE FILTERING
    # =============================================================

    @staticmethod
    def filter_by_categories(
        businesses: List[BusinessLead],
        categories: List[str]
    ) -> List[BusinessLead]:

        categories = [
            category.lower()
            for category in categories
        ]

        filtered = []

        for business in businesses:

            category = (
                business.category.lower()
                if business.category
                else ""
            )

            if any(
                allowed in category
                for allowed in categories
            ):
                filtered.append(business)

        return filtered

    # =============================================================
    # TOP N LEADS
    # =============================================================

    @staticmethod
    def top_leads(
        businesses: List[BusinessLead],
        limit: int = 25
    ) -> List[BusinessLead]:

        sorted_businesses = sorted(
            businesses,
            key=lambda x: x.lead_score.lead_score,
            reverse=True
        )

        return sorted_businesses[:limit]

