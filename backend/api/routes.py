"""
API Routes Module
=================
Defines all REST API endpoints for the Fake Review Detection system.

Endpoints:
- POST /analyze: Analyze reviews for a given Amazon product URL
- GET /product/{asin}: Get cached analysis results
- GET /status/{job_id}: Check analysis job status

Flow Diagram:
User -> POST /analyze -> Extract ASIN -> Fetch Reviews -> ML Pipeline -> Return Results
"""

import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
import time

from services.canopy_service import CanopyService
from services.analysis_service import AnalysisService
from utils.asin_extractor import extract_asin

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
canopy_service = CanopyService()
analysis_service = AnalysisService()


# ==================== Pydantic Models ====================
# These define the request/response structure for API validation

class AnalyzeRequest(BaseModel):
    """
    Request model for product analysis.
    Accepts an Amazon product URL.
    """
    url: str = Field(
        ..., 
        description="Amazon product URL (amazon.in supported)",
        examples=["https://www.amazon.in/dp/B08N5WRWNW"]
    )


class ReviewResult(BaseModel):
    """
    Individual review analysis result.
    Contains the classification and explanation.
    """
    review_id: str
    reviewer_name: str
    rating: float
    title: str
    text: str
    date: str
    verified_purchase: bool
    label: str  # "genuine" or "fake"
    confidence: float  # 0.0 to 1.0
    reasons: List[str]  # Explainable reasons for classification


class AnalysisMetrics(BaseModel):
    """
    Aggregated metrics for the product analysis.
    These are the key statistics shown on the dashboard.
    """
    total_reviews: int
    fake_count: int
    genuine_count: int
    fake_percentage: float
    original_rating: float
    adjusted_rating: float
    rating_difference: float
    authenticity_grade: str  # A, B, C, D, or F
    grade_description: str


class PatternInsight(BaseModel):
    """
    Detected pattern in fake reviews.
    Used to explain common issues found.
    """
    pattern_type: str
    description: str
    frequency: int


class AnalysisResponse(BaseModel):
    """
    Complete analysis response.
    Contains all data needed for the frontend dashboard.
    """
    success: bool
    asin: str
    product_title: str
    product_image: Optional[str]
    product_url: str
    analysis_date: str
    metrics: AnalysisMetrics
    patterns: List[PatternInsight]
    summary: str  # Human-readable summary
    reviews: List[ReviewResult]


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None


# ==================== API Endpoints ====================

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_product(request: AnalyzeRequest):
    """
    Main endpoint to analyze an Amazon product for fake reviews.
    
    Process:
    1. Extract ASIN from URL
    2. Fetch reviews from Bright Data API
    3. Run ML classification on each review
    4. Aggregate results and compute metrics
    5. Return complete analysis
    
    This endpoint may take 30-60 seconds depending on review count.
    """
    logger.info(f"📥 Received analysis request for URL: {request.url}")
    start_time = time.time()
    
    try:
        # Step 1: Extract ASIN from Amazon URL
        asin = extract_asin(request.url)
        if not asin:
            raise HTTPException(
                status_code=400,
                detail="Could not extract ASIN from URL. Please provide a valid Amazon product URL."
            )
        logger.info(f"✅ Extracted ASIN: {asin}")
        
        # Step 2: Fetch reviews from Canopy
        logger.info(f"🔄 Fetching reviews from Canopy for ASIN: {asin}")
        reviews_data, is_demo_data = await canopy_service.fetch_reviews(asin, request.url)
        
        if not reviews_data or len(reviews_data) == 0:
            raise HTTPException(
                status_code=404,
                detail="No reviews found for this product. Please try another product."
            )
        logger.info(f"✅ Fetched {len(reviews_data)} reviews")
        
        # Step 3 & 4: Analyze reviews using ML pipeline
        logger.info("🧠 Running ML analysis pipeline...")
        analysis_result = await analysis_service.analyze_reviews(
            asin=asin,
            url=request.url,
            reviews=reviews_data,
            is_demo_data=is_demo_data
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Analysis complete in {elapsed_time:.2f} seconds")
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/health")
async def api_health():
    """
    API health check endpoint.
    Useful for monitoring and debugging.
    """
    return {
        "status": "healthy",
        "services": {
            "canopy": canopy_service.is_configured(),
            "ml_pipeline": True
        }
    }


@router.get("/demo")
async def demo_analysis():
    """
    Demo endpoint with sample data.
    Useful for frontend development and testing without API calls.
    
    Note: This returns mock data - NOT for production use.
    """
    logger.info("📥 Demo analysis requested")
    
    # Return sample data for frontend testing
    return await analysis_service.get_demo_analysis()


@router.get("/test-canopy")
async def test_canopy():
    """
    Test Canopy API connection and response format.
    Helps debug API integration issues.
    """
    import httpx
    from config import settings
    
    logger.info("🧪 Testing Canopy API...")
    
    try:
        url = "https://rest.canopyapi.co/api/amazon/product/reviews"
        
        headers = {
            "API-KEY": settings.CANOPY_API_KEY,
            "Content-Type": "application/json"
        }
        
        params = {
            "asin": "B094NC89P9",
            "domain": "IN"
        }
        
        logger.info(f"📡 Sending request to: {url}")
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.get(url, headers=headers, params=params)
            
            logger.info(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                top_reviews = (
                    data.get("data", {})
                    .get("amazonProduct", {})
                    .get("topReviews", [])
                )
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "review_count": len(top_reviews),
                    "first_review": top_reviews[0] if top_reviews else None
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                }
                
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
