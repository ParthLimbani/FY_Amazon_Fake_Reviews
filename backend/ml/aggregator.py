"""
Results Aggregator
==================
Aggregates individual review classifications into product-level metrics.

Computes:
- Fake review percentage
- Adjusted rating (excluding fake reviews)
- Authenticity grade (A-F)
- Pattern analysis
- Summary generation

These metrics are displayed on the frontend dashboard.
"""

import logging
from typing import List, Dict, Any
from collections import Counter

logger = logging.getLogger(__name__)


class ResultsAggregator:
    """
    Aggregates classification results into product-level insights.
    
    Provides:
    - Statistical metrics
    - Pattern detection
    - Authenticity grading
    - Human-readable summaries
    """
    
    # Authenticity grade thresholds
    # Based on fake review percentage
    GRADE_THRESHOLDS = {
        'A': (0, 5),      # < 5% fake
        'B': (5, 15),     # 5-15% fake
        'C': (15, 30),    # 15-30% fake
        'D': (30, 50),    # 30-50% fake
        'F': (50, 100)    # > 50% fake
    }
    
    GRADE_DESCRIPTIONS = {
        'A': "Excellent authenticity - Very few suspicious reviews detected",
        'B': "Good authenticity - Minor concerns with some reviews",
        'C': "Moderate authenticity concerns - 15-30% suspicious reviews detected",
        'D': "Significant authenticity issues - Many suspicious reviews detected",
        'F': "Poor authenticity - Majority of reviews appear suspicious"
    }
    
    def __init__(self):
        """Initialize the aggregator."""
        logger.info("✅ Results Aggregator initialized")
    
    def calculate_metrics(self, classified_reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics from classified reviews.
        
        Args:
            classified_reviews: List of reviews with classification results
            
        Returns:
            Dictionary containing all computed metrics
            
        Metrics Computed:
        1. Total reviews analyzed
        2. Fake vs Genuine counts
        3. Fake percentage
        4. Original rating (all reviews)
        5. Adjusted rating (genuine reviews only)
        6. Rating difference
        7. Authenticity grade
        """
        total_reviews = len(classified_reviews)
        
        if total_reviews == 0:
            return self._empty_metrics()
        
        # Count fake vs genuine
        fake_reviews = [r for r in classified_reviews if r.get("label") == "fake"]
        genuine_reviews = [r for r in classified_reviews if r.get("label") == "genuine"]
        
        fake_count = len(fake_reviews)
        genuine_count = len(genuine_reviews)
        
        # Calculate fake percentage
        fake_percentage = (fake_count / total_reviews) * 100
        
        # Calculate original rating (average of all reviews)
        all_ratings = [r.get("rating", 0) for r in classified_reviews]
        original_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        
        # Calculate adjusted rating (genuine reviews only)
        genuine_ratings = [r.get("rating", 0) for r in genuine_reviews]
        adjusted_rating = sum(genuine_ratings) / len(genuine_ratings) if genuine_ratings else original_rating
        
        # Rating difference
        rating_difference = original_rating - adjusted_rating
        
        # Determine authenticity grade
        authenticity_grade = self._calculate_grade(fake_percentage)
        grade_description = self.GRADE_DESCRIPTIONS.get(authenticity_grade, "")
        
        return {
            "total_reviews": total_reviews,
            "fake_count": fake_count,
            "genuine_count": genuine_count,
            "fake_percentage": round(fake_percentage, 1),
            "original_rating": round(original_rating, 1),
            "adjusted_rating": round(adjusted_rating, 1),
            "rating_difference": round(rating_difference, 2),
            "authenticity_grade": authenticity_grade,
            "grade_description": grade_description
        }
    
    def _calculate_grade(self, fake_percentage: float) -> str:
        """
        Calculate authenticity grade based on fake percentage.
        
        Grading Scale:
        A: < 5% fake reviews (Excellent)
        B: 5-15% fake reviews (Good)
        C: 15-30% fake reviews (Fair)
        D: 30-50% fake reviews (Poor)
        F: > 50% fake reviews (Fail)
        """
        for grade, (min_pct, max_pct) in self.GRADE_THRESHOLDS.items():
            if min_pct <= fake_percentage < max_pct:
                return grade
        return 'F'
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics when no reviews available."""
        return {
            "total_reviews": 0,
            "fake_count": 0,
            "genuine_count": 0,
            "fake_percentage": 0.0,
            "original_rating": 0.0,
            "adjusted_rating": 0.0,
            "rating_difference": 0.0,
            "authenticity_grade": "N/A",
            "grade_description": "No reviews available for analysis"
        }
    
    def detect_patterns(self, classified_reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect common patterns in fake reviews.
        
        Args:
            classified_reviews: List of classified reviews with features
            
        Returns:
            List of pattern insights with type, description, and frequency
            
        Patterns Detected:
        1. Excessive positivity
        2. Short generic reviews
        3. Unverified purchases with 5 stars
        4. Marketing language
        5. Repetitive phrases
        """
        patterns = []
        fake_reviews = [r for r in classified_reviews if r.get("label") == "fake"]
        
        if not fake_reviews:
            return patterns
        
        # Pattern 1: Excessive positivity
        excessive_pos_count = sum(
            1 for r in fake_reviews 
            if r.get("features", {}).get("excessive_positivity", False)
        )
        if excessive_pos_count > 0:
            patterns.append({
                "pattern_type": "excessive_positivity",
                "description": "Reviews showing unnaturally positive sentiment without specific details",
                "frequency": excessive_pos_count
            })
        
        # Pattern 2: Short generic reviews
        short_generic_count = sum(
            1 for r in fake_reviews 
            if r.get("features", {}).get("is_short_review", False) and 
               r.get("features", {}).get("is_generic", False)
        )
        if short_generic_count > 0:
            patterns.append({
                "pattern_type": "short_generic",
                "description": "Short, generic reviews lacking product-specific information",
                "frequency": short_generic_count
            })
        
        # Pattern 3: Unverified 5-star reviews
        unverified_5star = sum(
            1 for r in fake_reviews 
            if not r.get("features", {}).get("is_verified_purchase", True) and
               r.get("rating", 0) == 5.0
        )
        if unverified_5star > 0:
            patterns.append({
                "pattern_type": "unverified_5star",
                "description": "5-star reviews from unverified purchases",
                "frequency": unverified_5star
            })
        
        # Pattern 4: Marketing language
        marketing_count = sum(
            1 for r in fake_reviews 
            if r.get("features", {}).get("has_marketing_language", False)
        )
        if marketing_count > 0:
            patterns.append({
                "pattern_type": "marketing_language",
                "description": "Reviews containing promotional or marketing language",
                "frequency": marketing_count
            })
        
        # Pattern 5: Repetitive phrases
        fake_phrase_count = sum(
            1 for r in fake_reviews 
            if r.get("features", {}).get("fake_phrase_count", 0) > 2
        )
        if fake_phrase_count > 0:
            patterns.append({
                "pattern_type": "repetitive_phrases",
                "description": "Similar phrasing or common fake review expressions",
                "frequency": fake_phrase_count
            })
        
        # Pattern 6: Excessive punctuation/caps
        punct_caps_count = sum(
            1 for r in fake_reviews 
            if r.get("features", {}).get("has_excessive_punctuation", False) or
               r.get("features", {}).get("has_excessive_caps", False)
        )
        if punct_caps_count > 0:
            patterns.append({
                "pattern_type": "excessive_emphasis",
                "description": "Excessive use of punctuation (!!!!) or capital letters",
                "frequency": punct_caps_count
            })
        
        # Sort by frequency (most common first)
        patterns.sort(key=lambda x: x["frequency"], reverse=True)
        
        return patterns
    
    def generate_summary(
        self, 
        metrics: Dict[str, Any], 
        patterns: List[Dict[str, Any]]
    ) -> str:
        """
        Generate human-readable analysis summary.
        
        This summary is displayed on the frontend to help users
        understand the analysis results at a glance.
        
        Args:
            metrics: Calculated metrics dictionary
            patterns: Detected patterns list
            
        Returns:
            Formatted summary string with key findings
        """
        total = metrics.get("total_reviews", 0)
        fake_pct = metrics.get("fake_percentage", 0)
        fake_count = metrics.get("fake_count", 0)
        genuine_count = metrics.get("genuine_count", 0)
        grade = metrics.get("authenticity_grade", "N/A")
        original_rating = metrics.get("original_rating", 0)
        adjusted_rating = metrics.get("adjusted_rating", 0)
        rating_diff = metrics.get("rating_difference", 0)
        
        if total == 0:
            return "No reviews were available for analysis."
        
        # Build summary based on grade
        if grade == 'A':
            tone = "This product has highly authentic reviews."
            recommendation = "The reviews appear trustworthy - you can rely on the displayed rating."
        elif grade == 'B':
            tone = "This product has generally authentic reviews with minor concerns."
            recommendation = "Most reviews appear genuine - the rating is fairly reliable."
        elif grade == 'C':
            tone = "This product shows moderate authenticity concerns."
            recommendation = "Exercise caution and focus on verified purchase reviews for accurate feedback."
        elif grade == 'D':
            tone = "This product has significant authenticity issues with its reviews."
            recommendation = "Be skeptical of the displayed rating - many reviews appear suspicious."
        else:  # F
            tone = "This product's reviews show major authenticity problems."
            recommendation = "The majority of reviews appear fake or incentivized - consider alternatives."
        
        # Key findings
        findings = []
        findings.append(f"- {fake_pct}% of reviews ({fake_count} out of {total}) show characteristics of fake or incentivized reviews")
        
        if rating_diff > 0.3:
            findings.append(f"- The adjusted rating (excluding suspicious reviews) drops from {original_rating} to {adjusted_rating} stars")
        elif rating_diff > 0:
            findings.append(f"- The adjusted rating is slightly lower at {adjusted_rating} stars (vs {original_rating} original)")
        
        # Top patterns
        if patterns:
            top_pattern = patterns[0]
            findings.append(f"- Most common issue: {top_pattern['description']}")
        
        # Compose summary
        summary = f"""Based on our analysis of {total} reviews, {tone}

**Key Findings:**
{chr(10).join(findings)}

**Recommendation:** {recommendation}"""
        
        return summary
    
    def get_rating_distribution(
        self, 
        classified_reviews: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, int]]:
        """
        Get rating distribution for genuine vs fake reviews.
        
        Useful for visualizing how fake reviews skew ratings.
        
        Returns:
            Dictionary with rating distribution for each category
        """
        genuine_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        fake_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for review in classified_reviews:
            rating = int(review.get("rating", 3))
            rating = max(1, min(5, rating))  # Clamp to 1-5
            
            if review.get("label") == "fake":
                fake_dist[rating] += 1
            else:
                genuine_dist[rating] += 1
        
        return {
            "genuine": genuine_dist,
            "fake": fake_dist
        }
