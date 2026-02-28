"""
Test script to verify Canopy API integration
Run this to test if the API is working correctly
"""

import asyncio
import sys
sys.path.append('D:/Parth/Coding/FY PROJECT/fake_review_v5_Canopy/backend')

from services.canopy_service import CanopyService

async def test_canopy():
    """Test the Canopy API with a sample Amazon URL"""
    
    service = CanopyService()
    
    print("=" * 60)
    print("Testing Canopy API Integration")
    print("=" * 60)
    
    # Check if configured
    if not service.is_configured():
        print("❌ Canopy API is NOT configured")
        print("Please set CANOPY_API_KEY in .env file")
        return
    
    print("✅ Canopy API is configured")
    print(f"🔑 Key: {service.api_key[:20]}...")
    
    # Test with an Indian Amazon product
    test_url = "https://www.amazon.in/dp/B094NC89P9"
    test_asin = "B094NC89P9"
    
    print(f"\n🔍 Testing with URL: {test_url}")
    print(f"📦 ASIN: {test_asin}")
    print("\n⏳ Fetching reviews...\n")
    
    try:
        reviews, is_demo = await service.fetch_reviews(test_asin, test_url)
        
        print("=" * 60)
        print(f"✅ SUCCESS! Fetched {len(reviews)} reviews (Demo: {is_demo})")
        print("=" * 60)
        
        if reviews:
            print("\n📄 Sample Review (first one):")
            print("-" * 60)
            first_review = reviews[0]
            print(f"Reviewer: {first_review.get('reviewer_name', 'N/A')}")
            print(f"Rating: {first_review.get('rating', 'N/A')} stars")
            print(f"Title: {first_review.get('title', 'N/A')}")
            print(f"Text: {first_review.get('text', 'N/A')[:200]}...")
            print(f"Verified: {first_review.get('verified_purchase', False)}")
            print("-" * 60)
            print(f"\n✅ Total reviews ready for ML analysis: {len(reviews)}")
        else:
            print("⚠️ No reviews returned (check API response format)")
            
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_canopy())
