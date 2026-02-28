"""
Analysis Service
================
Orchestrates the complete review analysis pipeline.

This service:
1. Preprocesses review text
2. Runs ML classification
3. Aggregates results
4. Generates insights and summaries

Design Pattern: Service Layer Pattern
- Separates business logic from API layer
- Makes testing and maintenance easier
- Allows for easy dependency injection
"""

import logging
from typing import List, Dict, Any
from datetime import datetime

from ml.classifier import FakeReviewClassifier
from ml.preprocessor import ReviewPreprocessor
from ml.aggregator import ResultsAggregator

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Main service for coordinating fake review analysis.
    
    Acts as the orchestrator between:
    - Preprocessing module
    - ML Classification module
    - Results Aggregation module
    """
    
    def __init__(self):
        """Initialize all ML pipeline components."""
        self.preprocessor = ReviewPreprocessor()
        self.classifier = FakeReviewClassifier()
        self.aggregator = ResultsAggregator()
        
        logger.info("✅ Analysis Service initialized")
    
    async def analyze_reviews(
        self, 
        asin: str, 
        url: str, 
        reviews: List[Dict[str, Any]],
        is_demo_data: bool = False
    ) -> Dict[str, Any]:
        """
        Complete analysis pipeline for product reviews.
        
        Args:
            asin: Product ASIN
            url: Original Amazon URL
            reviews: List of review dictionaries from Bright Data
            
        Returns:
            Complete analysis result dictionary
            
        Pipeline Steps:
        1. Preprocess each review (clean text, extract features)
        2. Classify each review using ML model
        3. Aggregate results (metrics, patterns, grade)
        4. Generate summary
        """
        logger.info(f"🔄 Starting analysis for {len(reviews)} reviews")
        
        # Step 1: Preprocess reviews
        logger.info("📝 Step 1: Preprocessing reviews...")
        preprocessed_reviews = []
        for review in reviews:
            processed = self.preprocessor.preprocess(review)
            preprocessed_reviews.append(processed)
        
        # Step 2: Classify each review
        logger.info("🤖 Step 2: Running ML classification...")
        classified_reviews = []
        for review in preprocessed_reviews:
            classification = self.classifier.classify(review)
            classified_reviews.append({
                **review,
                "label": classification["label"],
                "confidence": classification["confidence"],
                "reasons": classification["reasons"]
            })
        
        # Step 3: Aggregate results
        logger.info("📊 Step 3: Aggregating results...")
        metrics = self.aggregator.calculate_metrics(classified_reviews)
        patterns = self.aggregator.detect_patterns(classified_reviews)
        
        # Step 4: Generate summary
        logger.info("📝 Step 4: Generating analysis summary...")
        summary = self.aggregator.generate_summary(metrics, patterns)
        
        # Extract product info from first review
        product_title = reviews[0].get("product_title", "Amazon Product")
        product_image = reviews[0].get("product_image", "")
        
        # Build response
        response = {
            "success": True,
            "asin": asin,
            "product_title": product_title,
            "product_image": product_image,
            "product_url": url,
            "analysis_date": datetime.now().isoformat(),
            "metrics": metrics,
            "patterns": patterns,
            "summary": summary,
            "reviews": classified_reviews,
            "is_demo_data": is_demo_data
        }
        
        logger.info("✅ Analysis complete")
        return response
    
    async def get_demo_analysis(self) -> Dict[str, Any]:
        """
        Return demo analysis for frontend development.
        Uses sample data to demonstrate the complete response format.
        """
        demo_response = {
            "success": True,
            "asin": "B08N5WRWNW",
            "product_title": "Sample Wireless Bluetooth Headphones with Active Noise Cancellation",
            "product_image": "https://via.placeholder.com/300x300?text=Product+Image",
            "product_url": "https://www.amazon.in/dp/B08N5WRWNW",
            "analysis_date": datetime.now().isoformat(),
            "is_demo_data": True,
            "metrics": {
                "total_reviews": 150,
                "fake_count": 38,
                "genuine_count": 112,
                "fake_percentage": 25.3,
                "original_rating": 4.5,
                "adjusted_rating": 3.8,
                "rating_difference": 0.7,
                "authenticity_grade": "C",
                "grade_description": "Moderate authenticity concerns - 15-30% suspicious reviews detected"
            },
            "patterns": [
                {
                    "pattern_type": "excessive_positivity",
                    "description": "Multiple reviews showing unnaturally positive sentiment without specific details",
                    "frequency": 15
                },
                {
                    "pattern_type": "short_generic",
                    "description": "Short, generic reviews lacking product-specific information",
                    "frequency": 12
                },
                {
                    "pattern_type": "unverified_purchases",
                    "description": "High concentration of 5-star reviews from unverified purchases",
                    "frequency": 18
                },
                {
                    "pattern_type": "repetitive_phrases",
                    "description": "Similar phrasing detected across multiple reviews",
                    "frequency": 8
                }
            ],
            "summary": """Based on our analysis of 150 reviews, we've identified authenticity concerns with this product's reviews.

**Key Findings:**
- 25.3% of reviews (38 out of 150) show characteristics of fake or incentivized reviews
- The adjusted rating after removing suspicious reviews drops from 4.5 to 3.8 stars
- Most suspicious reviews are from unverified purchases with generic, overly positive content

**Recommendation:** Exercise caution when considering this product. Focus on verified purchase reviews with detailed, specific feedback for a more accurate picture of product quality.""",
            "reviews": [
                {
                    "review_id": "R1DEMO001",
                    "reviewer_name": "Verified Buyer",
                    "rating": 4.0,
                    "title": "Solid headphones with good ANC",
                    "text": "Been using these for 3 weeks. ANC works well on my commute. Battery lasts about 20 hours. Comfortable for long wear. Build quality is plastic but feels durable.",
                    "date": "2025-01-20",
                    "verified_purchase": True,
                    "label": "genuine",
                    "confidence": 0.89,
                    "reasons": ["Verified purchase", "Specific details provided", "Balanced sentiment"]
                },
                {
                    "review_id": "R1DEMO002",
                    "reviewer_name": "Happy User123",
                    "rating": 5.0,
                    "title": "BEST HEADPHONES EVER!!!!",
                    "text": "Amazing product! Best quality! Must buy! Perfect in every way! 5 stars!",
                    "date": "2025-01-19",
                    "verified_purchase": False,
                    "label": "fake",
                    "confidence": 0.94,
                    "reasons": ["Excessive positivity", "No specific details", "Unverified purchase", "Generic praise"]
                }
            ]
        }
        
        return demo_response
