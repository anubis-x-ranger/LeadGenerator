from typing import Dict, List
from config import config


class LeadScorer:

    def __init__(self):
        self.weights = config.lead_scoring

    def score_lead(self, business: Dict) -> Dict:

        score = 0
        reasons = []
        recommendations = []

        # =========================================================
        # NO WEBSITE
        # =========================================================

        if not business.get("website"):

            score += self.weights.no_website_score

            reasons.append("No website detected")

            recommendations.append(
                "Offer a modern mobile-first business website"
            )

        # =========================================================
        # FACEBOOK ONLY BUSINESS
        # =========================================================

        facebook = business.get("facebook", "")
        instagram = business.get("instagram", "")
        website = business.get("website", "")

        if (
            facebook and
            not website
        ):

            score += self.weights.facebook_only_score

            reasons.append("Facebook-only digital presence")

            recommendations.append(
                "Offer website + lead capture funnel"
            )

        # =========================================================
        # NO WHATSAPP
        # =========================================================

        if not business.get("has_whatsapp"):

            score += self.weights.no_whatsapp_score

            reasons.append("No WhatsApp integration")

            recommendations.append(
                "Offer WhatsApp automation system"
            )

        # =========================================================
        # HIGH REVIEW COUNT
        # =========================================================

        review_count = business.get("review_count", 0)

        if review_count >= 100:

            score += self.weights.high_reviews_score

            reasons.append(
                f"Strong market validation ({review_count} reviews)"
            )

        # =========================================================
        # HIGH RATING
        # =========================================================

        rating = business.get("rating", 0)

        if rating >= 4.5:

            score += self.weights.high_rating_score

            reasons.append(
                f"High customer satisfaction ({rating} stars)"
            )

        # =========================================================
        # BROKEN WEBSITE
        # =========================================================

        if business.get("website_broken"):

            score += self.weights.broken_website_score

            reasons.append("Broken or unreachable website")

            recommendations.append(
                "Offer website redesign + hosting"
            )

        # =========================================================
        # NO SSL
        # =========================================================

        if (
            business.get("website") and
            not business.get("has_ssl", True)
        ):

            score += 10

            reasons.append("Website missing SSL security")

            recommendations.append(
                "Offer HTTPS-secured modern website"
            )

        # =========================================================
        # NO BOOKING SYSTEM
        # =========================================================

        if (
            business.get("website") and
            not business.get("booking_detected")
        ):

            score += self.weights.no_booking_score

            reasons.append("No online booking system detected")

            recommendations.append(
                "Offer booking automation system"
            )

        # =========================================================
        # OUTDATED WEBSITE SIGNALS
        # =========================================================

        if business.get("outdated_website"):

            score += self.weights.outdated_website_score

            reasons.append("Outdated website detected")

            recommendations.append(
                "Offer conversion-focused redesign"
            )

        # =========================================================
        # WEAK SOCIAL PRESENCE
        # =========================================================

        social_count = 0

        socials = [
            business.get("facebook"),
            business.get("instagram"),
            business.get("linkedin"),
            business.get("youtube")
        ]

        for social in socials:
            if social:
                social_count += 1

        if social_count <= 1:

            score += self.weights.weak_social_presence_score

            reasons.append("Weak social media presence")

        # =========================================================
        # NORMALIZE SCORE
        # =========================================================

        score = min(score, self.weights.max_score)

        # =========================================================
        # OPPORTUNITY CLASSIFICATION
        # =========================================================

        if score >= 75:
            opportunity = "HIGH"

        elif score >= 45:
            opportunity = "MEDIUM"

        else:
            opportunity = "LOW"

        # =========================================================
        # PRIMARY SERVICE RECOMMENDATION
        # =========================================================

        primary_offer = self.generate_primary_offer(
            business
        )

        # =========================================================
        # FINAL OUTPUT
        # =========================================================

        business["lead_score"] = score

        business["opportunity"] = opportunity

        business["score_reasons"] = " | ".join(reasons)

        business["recommended_services"] = (
            " | ".join(set(recommendations))
        )

        business["primary_offer"] = primary_offer

        return business

    # =============================================================
    # SCORE BATCH
    # =============================================================

    def score_batch(
        self,
        businesses: List[Dict]
    ) -> List[Dict]:

        return [
            self.score_lead(business)
            for business in businesses
        ]

    # =============================================================
    # OFFER GENERATOR
    # =============================================================

    def generate_primary_offer(
        self,
        business: Dict
    ) -> str:

        if not business.get("website"):

            return "Business Website + WhatsApp Integration"

        if business.get("website_broken"):

            return "Website Redesign + Hosting"

        if not business.get("booking_detected"):

            return "Online Booking System"

        if not business.get("has_whatsapp"):

            return "WhatsApp Automation"

        if business.get("outdated_website"):

            return "Modern Conversion-Focused Redesign"

        return "Lead Generation Optimization"

