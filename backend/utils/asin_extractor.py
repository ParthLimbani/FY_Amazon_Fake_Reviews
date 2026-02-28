"""
ASIN Extractor Utility
======================
Extracts Amazon Standard Identification Number (ASIN) from various Amazon URL formats.

What is ASIN?
- ASIN is Amazon's unique product identifier
- 10-character alphanumeric code (e.g., B08N5WRWNW)
- Used to uniquely identify products across Amazon
- Essential for API calls to fetch product data

Supported URL Formats:
1. https://www.amazon.in/dp/B08N5WRWNW
2. https://www.amazon.in/product/B08N5WRWNW
3. https://www.amazon.in/Product-Name/dp/B08N5WRWNW/ref=...
4. https://www.amazon.in/gp/product/B08N5WRWNW
5. amazon.in/dp/B08N5WRWNW (without https)
"""

import re
import logging
from typing import Optional
from urllib.parse import urlparse, unquote

logger = logging.getLogger(__name__)


def extract_asin(url: str) -> Optional[str]:
    """
    Extract ASIN from an Amazon product URL.
    
    Args:
        url: Amazon product URL (any format)
        
    Returns:
        10-character ASIN string, or None if not found
        
    Examples:
        >>> extract_asin("https://www.amazon.in/dp/B08N5WRWNW")
        'B08N5WRWNW'
        >>> extract_asin("https://amazon.com/Product-Name/dp/B08N5WRWNW/ref=sr_1_1")
        'B08N5WRWNW'
    """
    if not url:
        logger.warning("Empty URL provided")
        return None
    
    # Decode URL-encoded characters
    url = unquote(url)
    
    # Remove any whitespace
    url = url.strip()
    
    # Add https if missing (for URL parsing)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Method 1: Match /dp/ASIN pattern (most common)
    dp_pattern = r'/dp/([A-Z0-9]{10})'
    match = re.search(dp_pattern, url, re.IGNORECASE)
    if match:
        asin = match.group(1).upper()
        logger.info(f"✅ Extracted ASIN via /dp/ pattern: {asin}")
        return asin
    
    # Method 2: Match /gp/product/ASIN pattern
    gp_pattern = r'/gp/product/([A-Z0-9]{10})'
    match = re.search(gp_pattern, url, re.IGNORECASE)
    if match:
        asin = match.group(1).upper()
        logger.info(f"✅ Extracted ASIN via /gp/product/ pattern: {asin}")
        return asin
    
    # Method 3: Match /product/ASIN pattern
    product_pattern = r'/product/([A-Z0-9]{10})'
    match = re.search(product_pattern, url, re.IGNORECASE)
    if match:
        asin = match.group(1).upper()
        logger.info(f"✅ Extracted ASIN via /product/ pattern: {asin}")
        return asin
    
    # Method 4: Match /ASIN/ pattern (fallback)
    asin_pattern = r'/([A-Z0-9]{10})(?:/|$|\?)'
    match = re.search(asin_pattern, url, re.IGNORECASE)
    if match:
        potential_asin = match.group(1).upper()
        # Validate it looks like an ASIN (starts with B or contains digits)
        if potential_asin.startswith('B') or any(c.isdigit() for c in potential_asin):
            logger.info(f"✅ Extracted ASIN via fallback pattern: {potential_asin}")
            return potential_asin
    
    # Method 5: Direct ASIN input (user may paste just the ASIN)
    if re.match(r'^[A-Z0-9]{10}$', url.upper()):
        asin = url.upper()
        logger.info(f"✅ Direct ASIN provided: {asin}")
        return asin
    
    logger.warning(f"❌ Could not extract ASIN from URL: {url}")
    return None


def validate_asin(asin: str) -> bool:
    """
    Validate that a string is a valid ASIN format.
    
    Args:
        asin: String to validate
        
    Returns:
        True if valid ASIN format, False otherwise
        
    ASIN Format:
    - Exactly 10 characters
    - Alphanumeric (letters and numbers)
    - Usually starts with 'B' for products
    """
    if not asin:
        return False
    
    # Must be exactly 10 characters
    if len(asin) != 10:
        return False
    
    # Must be alphanumeric
    if not asin.isalnum():
        return False
    
    return True


def build_amazon_url(asin: str, domain: str = "amazon.in") -> str:
    """
    Build a standard Amazon product URL from ASIN.
    
    Args:
        asin: Product ASIN
        domain: Amazon domain (default: amazon.in)
        
    Returns:
        Formatted Amazon product URL
    """
    return f"https://www.{domain}/dp/{asin}"


def get_amazon_domain(url: str) -> str:
    """
    Extract Amazon domain from URL.
    
    Args:
        url: Amazon URL
        
    Returns:
        Domain string (e.g., "amazon.in", "amazon.com")
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain if domain else "amazon.in"
    except Exception:
        return "amazon.in"


# Test function for development
if __name__ == "__main__":
    # Test various URL formats
    test_urls = [
        "https://www.amazon.in/dp/B08N5WRWNW",
        "https://www.amazon.in/Apple-iPhone-13-128GB-Midnight/dp/B09V3KXJPB/ref=sr_1_1",
        "https://amazon.in/gp/product/B08N5WRWNW",
        "amazon.in/dp/B08N5WRWNW",
        "B08N5WRWNW",
        "https://www.amazon.com/dp/B08N5WRWNW",
        "invalid-url"
    ]
    
    for url in test_urls:
        asin = extract_asin(url)
        print(f"URL: {url}")
        print(f"ASIN: {asin}")
        print("---")
