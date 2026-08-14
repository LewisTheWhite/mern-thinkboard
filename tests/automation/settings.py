"""
Configuration settings for test automation.
Loads environment variables and provides defaults for testing.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
ENV_FILE = Path(__file__).parent.parent.parent / ".env"
load_dotenv(ENV_FILE)


@dataclass
class APIConfig:
    """API configuration settings."""
    BASE_URL: str = os.getenv("TEST_API_BASE_URL", "http://localhost:5001/api")
    AUTH_BASE_URL: str = os.getenv("TEST_AUTH_BASE_URL", "http://localhost:5001/api/auth")
    NOTES_BASE_URL: str = os.getenv("TEST_NOTES_BASE_URL", "http://localhost:5001/api/notes")
    TIMEOUT: int = int(os.getenv("TEST_API_TIMEOUT", "30"))
    RETRIES: int = int(os.getenv("TEST_API_RETRIES", "3"))


@dataclass
class UIConfig:
    """UI/Browser configuration settings."""
    BROWSER_TYPE: str = os.getenv("TEST_BROWSER_TYPE", "chromium")
    BASE_URL: str = os.getenv("TEST_UI_BASE_URL", "http://localhost:5173")
    HEADLESS: bool = os.getenv("TEST_HEADLESS", "true").lower() == "true"
    SCREENSHOT_ON_FAILURE: bool = os.getenv("TEST_SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    TRACE_ON_FAILURE: bool = os.getenv("TEST_TRACE_ON_FAILURE", "false").lower() == "true"
    TIMEOUT: int = int(os.getenv("TEST_UI_TIMEOUT", "30000"))  # ms


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/notes_db")
    DB_NAME: str = os.getenv("TEST_DB_NAME", "notes_db_test")


@dataclass
class TestDataConfig:
    """Test data configuration."""
    TEST_USER_EMAIL_PREFIX: str = os.getenv("TEST_USER_EMAIL_PREFIX", "testuser")
    TEST_USER_NAME: str = os.getenv("TEST_USER_NAME", "Test User")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "TestPassword123!")
    TEST_PASSWORD_INVALID: str = "short"
    TEST_EMAIL_INVALID: str = "invalidemail"


@dataclass
class Config:
    """Global test configuration."""
    api: APIConfig = APIConfig()
    ui: UIConfig = UIConfig()
    database: DatabaseConfig = DatabaseConfig()
    test_data: TestDataConfig = TestDataConfig()
    LOG_LEVEL: str = os.getenv("TEST_LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("TEST_ENVIRONMENT", "local")


# Global config instance
config = Config()
