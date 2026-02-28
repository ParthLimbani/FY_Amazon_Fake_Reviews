"""
Review Preprocessor
===================
Handles text cleaning and feature extraction for reviews.

Preprocessing Steps:
1. Clean HTML and special characters
2. Normalize text (lowercase, remove extra spaces)
3. Extract text-based features
4. Extract metadata features

Why Preprocessing?
- Raw text contains noise that hurts model performance
- Consistent formatting improves classification accuracy
- Feature extraction captures patterns indicative of fake reviews
"""

import re
import logging
from typing import Dict, Any, List
from datetime import datetime

# Text analysis imports
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logging.warning("TextBlob not available. Sentiment analysis will be simplified.")

logger = logging.getLogger(__name__)


class ReviewPreprocessor:
    """
    Preprocesses review data for ML classification.
    
    Extracts both text-based and metadata-based features
    that are indicative of fake reviews.
    """
    
    # Common patterns in fake reviews
    FAKE_PHRASES = [
        "best product", "amazing product", "best ever", "must buy",
        "highly recommend", "5 stars", "perfect", "excellent quality",
        "love it", "awesome", "fantastic", "wonderful", "great product",
        "best purchase", "worth every penny", "changed my life",
        "everyone should buy", "no complaints", "buy it now",
        "best in market", "superior quality", "game changer"
    ]
    
    # Marketing language patterns
    MARKETING_PATTERNS = [
        r"buy\s*(it\s*)?now",
        r"limited\s*time",
        r"don'?t\s*miss",
        r"order\s*today",
        r"best\s*deal",
        r"free\s*shipping",
        r"act\s*fast"
    ]
    
    # Excessive punctuation pattern
    EXCESSIVE_PUNCT_PATTERN = re.compile(r'[!?]{2,}')
    
    # All caps pattern
    ALL_CAPS_PATTERN = re.compile(r'\b[A-Z]{4,}\b')
    
    def __init__(self):
        """Initialize the preprocessor."""
        logger.info("✅ Review Preprocessor initialized")
    
    def preprocess(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess a single review.
        
        Args:
            review: Raw review dictionary from Bright Data
            
        Returns:
            Enhanced review dictionary with extracted features
        """
        # Extract raw values
        raw_text = review.get("text", "")
        title = review.get("title", "")
        rating = review.get("rating", 3.0)
        verified = review.get("verified_purchase", False)
        
        # Clean text
        cleaned_text = self._clean_text(raw_text)
        cleaned_title = self._clean_text(title)
        
        # Combine title and text for analysis
        full_text = f"{cleaned_title} {cleaned_text}"
        
        # Extract features
        features = self._extract_features(
            text=cleaned_text,
            title=cleaned_title,
            full_text=full_text,
            rating=rating,
            verified=verified,
            raw_text=raw_text
        )
        
        # Return enhanced review
        return {
            **review,
            "cleaned_text": cleaned_text,
            "cleaned_title": cleaned_title,
            "features": features
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Steps:
        1. Remove HTML tags
        2. Remove URLs
        3. Normalize whitespace
        4. Handle encoding issues
        """
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _extract_features(
        self,
        text: str,
        title: str,
        full_text: str,
        rating: float,
        verified: bool,
        raw_text: str
    ) -> Dict[str, Any]:
        """
        Extract features indicative of fake reviews.
        
        Feature Categories:
        1. Text-based (length, complexity, patterns)
        2. Sentiment-based (polarity, subjectivity)
        3. Metadata-based (verified, rating)
        4. Behavioral (patterns, red flags)
        
        Returns:
            Dictionary of feature values
        """
        features = {}
        
        # === Text-based Features ===
        
        # Length features (short reviews are suspicious)
        features["text_length"] = len(text)
        features["word_count"] = len(text.split())
        features["title_length"] = len(title)
        
        # Short review flag (less than 50 chars is suspicious)
        features["is_short_review"] = len(text) < 50
        
        # Very long reviews are usually genuine (detailed feedback)
        features["is_detailed_review"] = len(text) > 300
        
        # === Pattern-based Features ===
        
        # Count fake phrases
        text_lower = full_text.lower()
        fake_phrase_count = sum(1 for phrase in self.FAKE_PHRASES if phrase in text_lower)
        features["fake_phrase_count"] = fake_phrase_count
        features["has_fake_phrases"] = fake_phrase_count > 2
        
        # Marketing language detection
        marketing_count = sum(
            1 for pattern in self.MARKETING_PATTERNS 
            if re.search(pattern, text_lower)
        )
        features["marketing_language_count"] = marketing_count
        features["has_marketing_language"] = marketing_count > 0
        
        # Excessive punctuation (e.g., "AMAZING!!!!!!")
        excessive_punct = len(self.EXCESSIVE_PUNCT_PATTERN.findall(raw_text))
        features["excessive_punctuation"] = excessive_punct
        features["has_excessive_punctuation"] = excessive_punct > 1
        
        # All caps words (shouting)
        all_caps_words = len(self.ALL_CAPS_PATTERN.findall(raw_text))
        features["all_caps_count"] = all_caps_words
        features["has_excessive_caps"] = all_caps_words > 2
        
        # Repetitive words (same word repeated many times)
        words = text_lower.split()
        if words:
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            max_repeat = max(word_freq.values()) if word_freq else 0
            features["max_word_repetition"] = max_repeat
            features["has_repetitive_words"] = max_repeat > 3
        else:
            features["max_word_repetition"] = 0
            features["has_repetitive_words"] = False
        
        # === Sentiment Features ===
        
        if TEXTBLOB_AVAILABLE and text:
            try:
                blob = TextBlob(text)
                features["sentiment_polarity"] = blob.sentiment.polarity  # -1 to 1
                features["sentiment_subjectivity"] = blob.sentiment.subjectivity  # 0 to 1
            except Exception:
                features["sentiment_polarity"] = 0.0
                features["sentiment_subjectivity"] = 0.5
        else:
            # Simplified sentiment (count positive/negative words)
            positive_words = ["good", "great", "excellent", "amazing", "love", "best", "perfect", "awesome"]
            negative_words = ["bad", "poor", "terrible", "awful", "worst", "hate", "broken", "useless"]
            
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            total = pos_count + neg_count
            if total > 0:
                features["sentiment_polarity"] = (pos_count - neg_count) / total
            else:
                features["sentiment_polarity"] = 0.0
            features["sentiment_subjectivity"] = 0.5
        
        # Sentiment-rating mismatch (e.g., positive text but low rating)
        sentiment = features["sentiment_polarity"]
        if rating >= 4 and sentiment < -0.3:
            features["sentiment_rating_mismatch"] = True
        elif rating <= 2 and sentiment > 0.3:
            features["sentiment_rating_mismatch"] = True
        else:
            features["sentiment_rating_mismatch"] = False
        
        # Excessive positivity (very high sentiment + 5 stars)
        features["excessive_positivity"] = (
            rating == 5.0 and 
            sentiment > 0.5 and 
            features.get("has_fake_phrases", False)
        )
        
        # === Metadata Features ===
        
        features["is_verified_purchase"] = verified
        features["rating"] = rating
        features["is_extreme_rating"] = rating == 5.0 or rating == 1.0
        
        # Generic review detection (lacks specific product details)
        specific_indicators = [
            "week", "month", "day", "hour", "minute",
            "bought", "purchased", "ordered", "received",
            "battery", "quality", "feature", "works", "doesn't work",
            "size", "color", "weight", "price", "value",
            "packaging", "delivery", "shipping", "arrived"
        ]
        specific_count = sum(1 for ind in specific_indicators if ind in text_lower)
        features["specificity_score"] = specific_count
        features["is_generic"] = specific_count < 2 and len(text) > 20
        
        # === Composite Red Flag Score ===
        
        red_flags = 0
        if not verified:
            red_flags += 2
        if features["is_short_review"]:
            red_flags += 1
        if features["has_fake_phrases"]:
            red_flags += 2
        if features["has_marketing_language"]:
            red_flags += 2
        if features["excessive_positivity"]:
            red_flags += 2
        if features["sentiment_rating_mismatch"]:
            red_flags += 1
        if features["is_generic"]:
            red_flags += 1
        if features["has_excessive_punctuation"]:
            red_flags += 1
        if features["has_excessive_caps"]:
            red_flags += 1
        
        features["red_flag_score"] = red_flags
        
        return features
    
    def batch_preprocess(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Preprocess multiple reviews.
        
        Args:
            reviews: List of raw review dictionaries
            
        Returns:
            List of preprocessed review dictionaries
        """
        return [self.preprocess(review) for review in reviews]
