"""
Canopy Service
==============
Handles all communication with the Canopy Amazon Reviews API.

Why Canopy?
- Provides structured Amazon review data in real-time
- Handles anti-bot measures and rate limiting
- Returns clean JSON data ready for processing
- Ethical: Uses official data collection methods

API Documentation: https://canopyapi.co
Endpoint: GET /api/amazon/product/reviews
"""

import logging
import httpx
from typing import List, Dict, Optional, Any
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)


class CanopyService:
    """
    Service class for fetching Amazon reviews via Canopy API.

    Uses the GET /api/amazon/product/reviews endpoint which returns
    results synchronously (no polling required).
    """

    def __init__(self):
        """Initialize the Canopy service with API credentials."""
        self.api_key = settings.CANOPY_API_KEY
        self.base_url = "https://rest.canopyapi.co"
        self.domain = "IN"  # Amazon India

        # Canopy is synchronous - 60 seconds is sufficient
        self.timeout = httpx.Timeout(60.0)

    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key) and len(self.api_key.strip()) > 10

    async def fetch_reviews(
        self, asin: str, product_url: str
    ) -> tuple[List[Dict[str, Any]], bool]:
        """
        Fetch reviews for a product from Canopy API.

        Args:
            asin: Amazon Standard Identification Number
            product_url: Full Amazon product URL (used for fallback info only)

        Returns:
            Tuple of (reviews list, is_demo_data boolean)

        Flow:
        1. Check API key is configured
        2. Call GET /api/amazon/product/reviews with ASIN
        3. Parse topReviews from response
        4. Standardize and return
        """
        logger.info(f"🔄 Starting Canopy fetch for ASIN: {asin}")

        if not self.is_configured():
            logger.warning("⚠️ Canopy API not configured, using sample data")
            return self._get_sample_reviews_for_product(asin, product_url), True

        try:
            reviews = await self._fetch_reviews_from_api(asin)

            if reviews and len(reviews) > 0:
                standardized = self._standardize_reviews(reviews)
                logger.info(f"✅ Fetched and standardized {len(standardized)} reviews")
                return standardized, False
            else:
                logger.warning("⚠️ No reviews returned from Canopy, using sample data")
                return self._get_sample_reviews_for_product(asin, product_url), True

        except Exception as e:
            logger.error(f"❌ Canopy API error: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            logger.info("📦 Falling back to sample reviews")
            return self._get_sample_reviews_for_product(asin, product_url), True

    async def _fetch_reviews_from_api(self, asin: str) -> Optional[List[Dict]]:
        """
        Call Canopy's GET /api/amazon/product/reviews endpoint.

        Canopy is fully synchronous — one call, direct response.
        No polling or snapshot IDs needed.
        """
        endpoint = f"{self.base_url}/api/amazon/product/reviews"

        headers = {
            "API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        params = {
            "asin": asin,
            "domain": self.domain
        }

        logger.info(f"📡 Calling Canopy API...")
        logger.info(f"🔗 Endpoint: {endpoint}")
        logger.info("🔑 API Key: configured ✓")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(endpoint, headers=headers, params=params)

            logger.info(f"📨 Response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # Canopy response shape:
                # { "data": { "amazonProduct": { "topReviews": [...] } } }
                top_reviews = (
                    data.get("data", {})
                    .get("amazonProduct", {})
                    .get("topReviews", [])
                )

                logger.info(f"📊 Received {len(top_reviews)} reviews from Canopy")

                # Cap at 100 reviews
                return top_reviews[:100]

            elif response.status_code == 400:
                logger.error(f"❌ Canopy input validation error: {response.text}")
                return None

            elif response.status_code == 401:
                logger.error("❌ Canopy API key is invalid or unauthorized")
                return None

            else:
                logger.error(
                    f"❌ Canopy API error: {response.status_code} - {response.text[:300]}"
                )
                return None

    def _standardize_reviews(self, reviews: List[Dict]) -> List[Dict[str, Any]]:
        """
        Standardize Canopy review data to our internal format.

        Canopy review fields:
        - id, title, body, rating, helpfulVotes, verifiedPurchase
        - imageUrls (list), videos (list)
        - reviewer: { id, name, url }
        """
        standardized = []
        for i, review in enumerate(reviews):
            try:
                parsed = self._parse_single_review(review, i)
                if parsed:
                    standardized.append(parsed)
            except Exception as e:
                logger.warning(f"⚠️ Failed to parse review {i}: {e}")
                continue

        logger.info(f"📊 Standardized {len(standardized)} reviews")
        return standardized

    def _parse_single_review(
        self, review: Dict, index: int
    ) -> Optional[Dict[str, Any]]:
        """
        Parse a single Canopy review into our standardized format.

        Canopy field → Our field mapping:
        - id            → review_id
        - title         → title
        - body          → text
        - rating        → rating
        - helpfulVotes  → helpful_votes
        - verifiedPurchase → verified_purchase
        - reviewer.name → reviewer_name
        - imageUrls     → images
        """
        try:
            # Rating — guard against None
            rating = float(review.get("rating") or 3.0)

            # Review text — guard against None
            text = review.get("body") or ""

            # Title — guard against None
            title = review.get("title") or ""

            # Reviewer name (nested under reviewer object)
            reviewer = review.get("reviewer") or {}
            reviewer_name = reviewer.get("name") or "Anonymous"

            # Canopy does not return a review date in topReviews
            date = str(datetime.now().date())

            # Verified purchase — guard against None
            verified = bool(review.get("verifiedPurchase") or False)

            # Helpful votes — guard against None
            helpful = int(review.get("helpfulVotes") or 0)

            # Images — guard against None
            images = review.get("imageUrls") or []

            return {
                "review_id": review.get("id", f"review_{index}"),
                "reviewer_name": reviewer_name,
                "rating": rating,
                "title": title,
                "text": text,
                "date": date,
                "verified_purchase": verified,
                "helpful_votes": helpful,
                "images": images,
                "product_title": "",
                "product_image": ""
            }

        except Exception as e:
            logger.warning(f"⚠️ Error parsing review at index {index}: {e}")
            return None

    def _get_sample_reviews(self) -> List[Dict[str, Any]]:
        """
        Return sample reviews for development/demo mode.

        IMPORTANT: Synthetic data only. Real analysis requires API key.
        Includes a mix of genuine and fake patterns for testing the ML model.
        """
        sample_reviews = [
            # --- Genuine reviews (varied, specific, balanced) ---
            {
                "review_id": "R1GENUINE001",
                "reviewer_name": "Priya Sharma",
                "rating": 4.0,
                "title": "Good product but some minor issues",
                "text": "I've been using this for about 3 weeks now. The build quality is decent and it works as advertised. However, I noticed the battery life is slightly less than claimed - getting about 6 hours instead of 8. The sound quality is good for the price point. Delivery was on time. Would recommend for casual use but maybe look elsewhere for professional use.",
                "date": "2025-01-15",
                "verified_purchase": True,
                "helpful_votes": 12,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE002",
                "reviewer_name": "Rajesh Kumar",
                "rating": 3.0,
                "title": "Average performance, not worth the hype",
                "text": "After reading all the positive reviews, I had high expectations. Reality is it's just an average product. Does the job but nothing special. The packaging was nice but the product itself feels a bit cheap. I've used similar products from other brands that were better. Not bad, but not great either.",
                "date": "2025-01-10",
                "verified_purchase": True,
                "helpful_votes": 8,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE003",
                "reviewer_name": "Anita Desai",
                "rating": 5.0,
                "title": "Exceeded expectations!",
                "text": "Bought this after comparing with 3 other similar products. This one stood out for the features vs price ratio. Setup took about 30 minutes following the manual. Been using for 2 months and no issues. The customer support was helpful when I had questions about settings. Only minor complaint is the cable could be longer.",
                "date": "2025-01-08",
                "verified_purchase": True,
                "helpful_votes": 25,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE004",
                "reviewer_name": "Vikram Singh",
                "rating": 2.0,
                "title": "Disappointed with quality",
                "text": "Received the product and was immediately disappointed. The photos online looked much better. Material feels flimsy and I doubt it will last long. Tried contacting seller but no response yet. Expected much better for this price range.",
                "date": "2025-01-05",
                "verified_purchase": True,
                "helpful_votes": 15,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE005",
                "reviewer_name": "Meera Patel",
                "rating": 4.0,
                "title": "Solid purchase with minor quirks",
                "text": "Used this for a month before reviewing. Overall satisfied. The product does what it claims. Setup was straightforward. A few things could be better - the instructions were confusing in parts and the app could use improvement. But for the price, it's a fair deal. Would buy again.",
                "date": "2025-01-12",
                "verified_purchase": True,
                "helpful_votes": 18,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE006",
                "reviewer_name": "Arjun Nair",
                "rating": 4.0,
                "title": "Good for beginners",
                "text": "As someone new to this category, I found this product easy to use. It's not the most advanced option but perfect for starting out. The learning curve is gentle and the results are satisfactory. Might upgrade to a better model later but for now this serves my needs well.",
                "date": "2025-01-11",
                "verified_purchase": True,
                "helpful_votes": 10,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1GENUINE007",
                "reviewer_name": "Deepak Reddy",
                "rating": 3.0,
                "title": "Mixed feelings",
                "text": "There are things I like and dislike about this product. The design is sleek and modern. Performance is adequate. But it heats up quickly during extended use which is concerning. Also the warranty process seems complicated. It's okay for the price but don't expect miracles.",
                "date": "2025-01-09",
                "verified_purchase": True,
                "helpful_votes": 22,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            # --- Fake reviews (suspicious patterns) ---
            {
                "review_id": "R1FAKE001",
                "reviewer_name": "Happy Customer123",
                "rating": 5.0,
                "title": "BEST PRODUCT EVER!!!",
                "text": "Amazing product! Best quality! Must buy! Everyone should buy this! 5 stars! Perfect in every way! No complaints at all! Buy it now! You won't regret it! Best purchase ever! Highly recommended! A+++! Super happy!",
                "date": "2025-01-20",
                "verified_purchase": False,
                "helpful_votes": 0,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1FAKE002",
                "reviewer_name": "Review Verified User",
                "rating": 5.0,
                "title": "Perfect product must buy immediately",
                "text": "This product is perfect. I am very satisfied customer. The quality is best. Everyone in my family loves it. We bought 10 more for gifts. Best value for money. No other product compares. Buy without thinking!",
                "date": "2025-01-19",
                "verified_purchase": False,
                "helpful_votes": 1,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1FAKE003",
                "reviewer_name": "John D.",
                "rating": 5.0,
                "title": "Excellent",
                "text": "Good product. Nice quality. Fast delivery. Recommended.",
                "date": "2025-01-18",
                "verified_purchase": False,
                "helpful_votes": 0,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1FAKE004",
                "reviewer_name": "Satisfied Buyer",
                "rating": 5.0,
                "title": "Worth every penny",
                "text": "Best product in market. Superior quality than competitors. My life changed after using this. Cannot imagine living without it now. Every home needs one. Revolutionary product. Game changer. Innovation at its best!",
                "date": "2025-01-17",
                "verified_purchase": False,
                "helpful_votes": 2,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
            {
                "review_id": "R1FAKE005",
                "reviewer_name": "TestReviewer",
                "rating": 5.0,
                "title": "Amazing Amazing Amazing",
                "text": "Amazing product amazing quality amazing price amazing delivery amazing packaging amazing everything. What more can I say? Just amazing!",
                "date": "2025-01-16",
                "verified_purchase": False,
                "helpful_votes": 0,
                "images": [],
                "product_title": "",
                "product_image": ""
            },
        ]
        return sample_reviews

    def _get_sample_reviews_for_product(
        self, asin: str, product_url: str
    ) -> List[Dict[str, Any]]:
        """
        Return sample reviews tagged with the actual ASIN/URL for demo mode.
        """
        sample_reviews = self._get_sample_reviews()
        product_title = f"Amazon Product (ASIN: {asin})"
        product_image = ""

        for review in sample_reviews:
            review["product_title"] = product_title
            review["product_image"] = product_image
            review["asin"] = asin
            review["product_url"] = product_url

        logger.info(f"📦 Generated sample reviews for ASIN: {asin}")
        return sample_reviews
