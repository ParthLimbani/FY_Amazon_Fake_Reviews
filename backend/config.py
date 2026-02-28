"""
Configuration Module
====================
Centralizes all configuration settings using environment variables.
This follows the 12-factor app methodology for configuration management.

Why environment variables?
- Security: API keys are not committed to version control
- Flexibility: Different configurations for dev/prod environments
- Best Practice: Industry standard for sensitive data management
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.
    All sensitive data (API keys, credentials) should be stored
    in a .env file (not committed to git).
    """
    
    # Canopy API Configuration
    # These credentials are used to fetch Amazon reviews
    # SECURITY: Never commit API keys! Use .env file (see .env.example)
    CANOPY_API_KEY: str = os.getenv("CANOPY_API_KEY", "")
    
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ML Model Settings
    MODEL_CONFIDENCE_THRESHOLD: float = float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", "0.5"))
    
    # Rate Limiting (to avoid API abuse)
    MAX_REVIEWS_PER_REQUEST: int = int(os.getenv("MAX_REVIEWS_PER_REQUEST", "500"))
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validates that required settings are configured.
        Returns True if all required settings are present.
        """
        if not cls.CANOPY_API_KEY:
            print("⚠️ Warning: CANOPY_API_KEY not set.")
            print("   Please add your Canopy API key to the .env file.")
            print("   API calls will fall back to demo data.")
            return False
        return True


# Global settings instance
settings = Settings()
