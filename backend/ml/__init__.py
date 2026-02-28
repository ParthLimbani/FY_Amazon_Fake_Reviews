"""
ML Module
=========
Contains all machine learning components for fake review detection.

Components:
- preprocessor: Text cleaning and feature extraction
- classifier: ML model and rule-based classification
- aggregator: Results aggregation and metrics calculation
"""

from .preprocessor import ReviewPreprocessor
from .classifier import FakeReviewClassifier
from .aggregator import ResultsAggregator

__all__ = ["ReviewPreprocessor", "FakeReviewClassifier", "ResultsAggregator"]
