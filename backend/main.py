"""
Fake Review Detection API - Main Entry Point
=============================================
This is the main FastAPI application that serves as the entry point for
the Fake Review Detection system. It handles:
- API routing
- CORS configuration
- Application lifecycle events

Author: FY Project Team
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import router as api_router
from ml.classifier import FakeReviewClassifier

# Configure logging for debugging and viva explanation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global classifier instance (loaded once at startup)
classifier = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    - Loads ML model at startup
    - Cleans up resources at shutdown
    
    This pattern ensures the model is loaded only once,
    improving response times for subsequent requests.
    """
    global classifier
    logger.info("🚀 Starting Fake Review Detection API...")
    
    # Initialize the ML classifier
    classifier = FakeReviewClassifier()
    logger.info("✅ ML Classifier initialized successfully")
    
    yield  # Application runs here
    
    # Cleanup on shutdown
    logger.info("🛑 Shutting down Fake Review Detection API...")


# Create FastAPI application instance
app = FastAPI(
    title="Fake Review Detection API",
    description="""
    ## Fake Review Detection System
    
    This API analyzes Amazon product reviews to detect fake/suspicious reviews
    using a hybrid approach combining:
    - Machine Learning (TF-IDF + Logistic Regression)
    - Rule-based heuristics (text patterns, metadata signals)
    
    ### Key Features:
    - Fetches real reviews from Bright Data API
    - Classifies reviews as Genuine or Fake
    - Provides explainable reasons for each classification
    - Calculates adjusted ratings and authenticity grades
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend communication
# This allows the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """
    Health check endpoint.
    Returns basic API information.
    """
    return {
        "message": "Fake Review Detection API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check for monitoring.
    Useful for deployment health probes.
    """
    return {
        "status": "healthy",
        "classifier_loaded": classifier is not None
    }
