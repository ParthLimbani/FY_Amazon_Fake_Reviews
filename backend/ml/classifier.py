"""
Fake Review Classifier
======================
Hybrid ML + Rule-based classifier for detecting fake reviews.

Classification Approach:
1. Rule-based scoring for clear patterns
2. ML model (TF-IDF + Logistic Regression) for complex cases
3. Combine signals for final classification

Why Hybrid Approach?
- Rules catch obvious fake patterns with high confidence
- ML model handles nuanced cases
- Explainability: We can show exactly why a review was flagged
- Modular: Easy to upgrade ML model later

Model Architecture:
- TF-IDF Vectorizer: Converts text to numerical features
- Logistic Regression: Binary classifier (fake vs genuine)
- Rule Engine: Pattern-based scoring system
"""

import logging
import pickle
import os
from typing import Dict, Any, List, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class FakeReviewClassifier:
    """
    Hybrid classifier for fake review detection.
    
    Combines:
    1. Rule-based heuristics for explainability
    2. ML model for pattern recognition
    3. Confidence scoring for uncertainty
    """
    
    def __init__(self):
        """
        Initialize the classifier.
        
        Note: For a production system, you would train the ML model
        on labeled data. Here we use a rule-based approach that
        can be enhanced with a trained model.
        """
        self.model = None
        self.vectorizer = None
        
        # Try to load pre-trained model if available
        self._load_model()
        
        logger.info("✅ Fake Review Classifier initialized")
    
    def _load_model(self):
        """
        Load pre-trained model if available.
        
        For this project, we start with rule-based classification.
        Model can be trained and saved for production use.
        """
        model_path = os.path.join(os.path.dirname(__file__), "models", "classifier.pkl")
        vectorizer_path = os.path.join(os.path.dirname(__file__), "models", "vectorizer.pkl")
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                logger.info("✅ Loaded pre-trained ML model")
            except Exception as e:
                logger.warning(f"⚠️ Could not load model: {e}")
                self.model = None
                self.vectorizer = None
        else:
            logger.info("ℹ️ No pre-trained model found. Using rule-based classification.")
    
    def classify(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a single review as genuine or fake.
        
        Args:
            review: Preprocessed review with features
            
        Returns:
            Classification result with:
            - label: "genuine" or "fake"
            - confidence: 0.0 to 1.0
            - reasons: List of explanations
            
        Classification Logic:
        1. Apply rule-based scoring
        2. If ML model available, combine with ML prediction
        3. Generate explanation reasons
        """
        features = review.get("features", {})
        text = review.get("cleaned_text", "")
        
        # Step 1: Rule-based scoring
        rule_score, rule_reasons = self._apply_rules(features, text)
        
        # Step 2: ML model scoring (if available)
        if self.model and self.vectorizer and text:
            ml_score = self._ml_predict(text)
            # Combine rule and ML scores (weighted average)
            # Rule-based gets more weight for explainability
            combined_score = 0.6 * rule_score + 0.4 * ml_score
        else:
            combined_score = rule_score
        
        # Step 3: Determine label and confidence
        if combined_score >= 0.5:
            label = "fake"
            confidence = min(0.99, combined_score)
        else:
            label = "genuine"
            confidence = min(0.99, 1 - combined_score)
        
        # Step 4: Generate reasons for classification
        if label == "genuine":
            reasons = self._get_genuine_reasons(features)
        else:
            reasons = rule_reasons if rule_reasons else ["Suspicious patterns detected"]
        
        return {
            "label": label,
            "confidence": round(confidence, 2),
            "reasons": reasons
        }
    
    def _apply_rules(self, features: Dict[str, Any], text: str) -> Tuple[float, List[str]]:
        """
        Apply rule-based classification.
        
        Returns:
            Tuple of (score, reasons)
            - score: 0.0 (definitely genuine) to 1.0 (definitely fake)
            - reasons: List of reasons for the score
            
        Rules are based on academic research on fake review detection:
        - Mukherjee et al. (2013) - "What Yelp Fake Review Filter Might Be Doing"
        - Jindal & Liu (2008) - "Opinion Spam and Analysis"
        """
        score = 0.0
        reasons = []
        
        # Rule 1: Unverified purchase (major red flag)
        if not features.get("is_verified_purchase", True):
            score += 0.25
            reasons.append("Unverified purchase")
        
        # Rule 2: Short generic reviews
        if features.get("is_short_review", False) and features.get("is_generic", False):
            score += 0.2
            reasons.append("Short, generic review without specific details")
        elif features.get("is_short_review", False):
            score += 0.1
            reasons.append("Very short review")
        
        # Rule 3: Excessive fake phrases
        fake_count = features.get("fake_phrase_count", 0)
        if fake_count > 3:
            score += 0.25
            reasons.append(f"Contains {fake_count} common fake review phrases")
        elif fake_count > 1:
            score += 0.1
            reasons.append("Contains promotional language")
        
        # Rule 4: Marketing language
        if features.get("has_marketing_language", False):
            score += 0.15
            reasons.append("Contains marketing/promotional language")
        
        # Rule 5: Excessive positivity without substance
        if features.get("excessive_positivity", False):
            score += 0.2
            reasons.append("Excessive positivity without specific details")
        
        # Rule 6: Sentiment-rating mismatch
        if features.get("sentiment_rating_mismatch", False):
            score += 0.15
            reasons.append("Sentiment does not match star rating")
        
        # Rule 7: Excessive punctuation/caps (!!!!! or AMAZING)
        if features.get("has_excessive_punctuation", False):
            score += 0.1
            reasons.append("Excessive punctuation usage")
        if features.get("has_excessive_caps", False):
            score += 0.1
            reasons.append("Excessive use of capital letters")
        
        # Rule 8: Generic review content
        if features.get("is_generic", False) and features.get("rating", 3) == 5:
            score += 0.15
            reasons.append("Generic 5-star review lacking specific feedback")
        
        # Rule 9: Repetitive words
        if features.get("has_repetitive_words", False):
            score += 0.1
            reasons.append("Repetitive word usage")
        
        # === Genuine indicators (reduce score) ===
        
        # Verified purchase with detailed review
        if features.get("is_verified_purchase", False) and features.get("is_detailed_review", False):
            score -= 0.2
        
        # High specificity score
        if features.get("specificity_score", 0) > 4:
            score -= 0.15
        
        # Balanced rating (not extreme)
        if not features.get("is_extreme_rating", True):
            score -= 0.1
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, score))
        
        return score, reasons
    
    def _ml_predict(self, text: str) -> float:
        """
        Get ML model prediction probability.
        
        Args:
            text: Cleaned review text
            
        Returns:
            Probability of being fake (0.0 to 1.0)
        """
        if not self.model or not self.vectorizer:
            return 0.5  # Neutral if no model
        
        try:
            # Vectorize the text
            X = self.vectorizer.transform([text])
            
            # Get probability of fake class
            proba = self.model.predict_proba(X)[0]
            
            # Return probability of fake (assuming fake is class 1)
            return proba[1] if len(proba) > 1 else proba[0]
        except Exception as e:
            logger.warning(f"⚠️ ML prediction failed: {e}")
            return 0.5
    
    def _get_genuine_reasons(self, features: Dict[str, Any]) -> List[str]:
        """
        Generate reasons why a review is classified as genuine.
        
        Used for transparency in showing positive signals.
        """
        reasons = []
        
        if features.get("is_verified_purchase", False):
            reasons.append("Verified purchase")
        
        if features.get("is_detailed_review", False):
            reasons.append("Detailed review with specific information")
        
        if features.get("specificity_score", 0) > 3:
            reasons.append("Contains specific product details")
        
        if not features.get("is_extreme_rating", True):
            reasons.append("Balanced rating (not extreme)")
        
        # Sentiment matches rating
        if not features.get("sentiment_rating_mismatch", False):
            reasons.append("Sentiment consistent with rating")
        
        if not reasons:
            reasons.append("No suspicious patterns detected")
        
        return reasons
    
    def batch_classify(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classify multiple reviews.
        
        Args:
            reviews: List of preprocessed reviews
            
        Returns:
            List of classification results
        """
        return [self.classify(review) for review in reviews]


# === Model Training Functions ===
# These functions are used to train the ML model on labeled data

def train_classifier(labeled_reviews: List[Dict[str, Any]]) -> Tuple[Any, Any]:
    """
    Train TF-IDF + Logistic Regression classifier.
    
    Args:
        labeled_reviews: List of reviews with 'text' and 'label' fields
        
    Returns:
        Tuple of (trained_model, vectorizer)
        
    Usage:
        labeled_data = [
            {"text": "Great product!", "label": "genuine"},
            {"text": "Best ever buy now!", "label": "fake"},
            ...
        ]
        model, vectorizer = train_classifier(labeled_data)
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    
    # Extract texts and labels
    texts = [r['text'] for r in labeled_reviews]
    labels = [1 if r['label'] == 'fake' else 0 for r in labeled_reviews]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    # Create TF-IDF features
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english'
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train logistic regression
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    logger.info("\n" + classification_report(y_test, y_pred, target_names=['genuine', 'fake']))
    
    return model, vectorizer


def save_model(model, vectorizer, model_dir: str = None):
    """
    Save trained model and vectorizer to disk.
    
    Args:
        model: Trained classifier
        vectorizer: Fitted TF-IDF vectorizer
        model_dir: Directory to save models (default: ml/models/)
    """
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(__file__), "models")
    
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, "classifier.pkl")
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    logger.info(f"✅ Model saved to {model_dir}")
