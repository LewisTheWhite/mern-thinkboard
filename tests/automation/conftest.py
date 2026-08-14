"""
Pytest configuration and global fixtures.
Provides session, function, and autouse fixtures for all tests.
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import dotenv_values
from faker import Faker
from pymongo import MongoClient
from playwright.async_api import async_playwright

from api.client import APIClient
from api.endpoints import AUTH
from settings import config

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

fake = Faker()

pytest_plugins = ["fixtures.auth_fixtures"]


def _resolve_mongo_uri():
    """Resolve Mongo URI from env, backend/.env, or test config default."""
    from_env = os.getenv("MONGO_URI")
    if from_env:
        return from_env.strip().strip('"').strip("'")

    backend_env_path = Path(__file__).resolve().parents[2] / "backend" / ".env"
    if backend_env_path.exists():
        backend_env = dotenv_values(backend_env_path)
        backend_uri = backend_env.get("MONGO_URI")
        if backend_uri:
            return str(backend_uri).strip().strip('"').strip("'")

    fallback_uri = config.database.MONGO_URI
    if fallback_uri:
        return fallback_uri.strip().strip('"').strip("'")

    return ""


def _get_db_name_from_uri(uri: str) -> str:
    """Extract DB name from URI path as fallback when default database is unavailable."""
    try:
        db_name = uri.rsplit("/", 1)[-1].split("?", 1)[0]
        return db_name or config.database.DB_NAME
    except Exception:
        return config.database.DB_NAME


# ==================== SESSION FIXTURES ====================
@pytest.fixture(scope="session")
def session_config():
    """Provide config object for entire test session."""
    logger.info(f"Starting test session in {config.ENVIRONMENT} environment")
    yield config
    logger.info("Test session completed")


# ==================== FUNCTION FIXTURES ====================
@pytest.fixture(scope="function")
def api_client():
    """Provide API client for tests."""
    client = APIClient(base_url=config.api.BASE_URL)
    yield client
    client.close()


@pytest.fixture(scope="function")
def auth_api_client():
    """Provide authenticated API client after login."""
    client = APIClient(base_url=config.api.BASE_URL)
    yield client
    client.close()


@pytest.fixture(scope="function")
def test_email():
    """Generate unique test email."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    email = f"{config.test_data.TEST_USER_EMAIL_PREFIX}_{timestamp}_{fake.random_int(1000, 9999)}@test.com"
    return email


@pytest.fixture(scope="function")
def test_user_data(test_email):
    """Generate test user data."""
    return {
        "name": config.test_data.TEST_USER_NAME,
        "email": test_email,
        "password": config.test_data.TEST_PASSWORD,
        "confirmPassword": config.test_data.TEST_PASSWORD,
    }


@pytest.fixture(scope="function")
def test_note_data():
    """Generate test note data."""
    return {
        "title": f"Test Note - {fake.word()}",
        "content": fake.paragraph(nb_sentences=5),
    }


# ==================== BROWSER FIXTURES ====================
@pytest_asyncio.fixture(scope="function", autouse=False)
async def browser():
    """Provide Playwright browser instance."""
    async with async_playwright() as p:
        browser = await p[config.ui.BROWSER_TYPE].launch(
            headless=config.ui.HEADLESS
        )
        yield browser
        await browser.close()


@pytest_asyncio.fixture(scope="function", autouse=False)
async def browser_context(browser):
    """Provide Playwright browser context with viewport."""
    context = await browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    await context.close()


@pytest_asyncio.fixture(scope="function", autouse=False)
async def page(browser_context):
    """Provide Playwright page instance."""
    page = await browser_context.new_page()
    yield page
    await page.close()


# ==================== CLEANUP/TEARDOWN ====================
@pytest.fixture(scope="function", autouse=True)
def test_tracker(request):
    """Track and log test execution."""
    logger.info(f"Starting test: {request.node.name}")
    start_time = datetime.now()
    
    yield
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Completed test: {request.node.name} (Duration: {duration:.2f}s)")


@pytest.fixture(scope="function", autouse=True)
def ensure_test_user_exists(api_client: APIClient):
    """Ensure there is at least one test user created for each test run."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    ensure_user_payload = {
        "name": config.test_data.TEST_USER_NAME,
        "email": f"{config.test_data.TEST_USER_EMAIL_PREFIX}_seed_{timestamp}_{fake.random_int(1000, 9999)}@test.com",
        "password": config.test_data.TEST_PASSWORD,
        "confirmPassword": config.test_data.TEST_PASSWORD,
    }

    response = api_client.post(AUTH.SIGNUP, json=ensure_user_payload)
    assert response.status_code in (201, 409), f"Failed to ensure test user: {response.text}"


@pytest.fixture(scope="function", autouse=True)
def cleanup_test_data_after_test():
    """Delete test-created users and their dependent notes/labels after each test."""
    yield

    mongo_uri = _resolve_mongo_uri()
    if not mongo_uri or "user:pass@cluster.mongodb.net" in mongo_uri:
        logger.warning("Skipping DB cleanup: MONGO_URI is not configured for this environment")
        return

    email_prefix = config.test_data.TEST_USER_EMAIL_PREFIX
    email_regex = rf"^{re.escape(email_prefix)}_"

    client = None
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")

        db = client.get_default_database()
        if db is None:
            db = client[_get_db_name_from_uri(mongo_uri)]

        users_cursor = db.users.find({"email": {"$regex": email_regex}}, {"_id": 1})
        user_ids = [user["_id"] for user in users_cursor]

        if not user_ids:
            return

        notes_deleted = db.notes.delete_many({"userId": {"$in": user_ids}}).deleted_count
        labels_deleted = db.labels.delete_many({"userId": {"$in": user_ids}, "isDefault": {"$ne": True}}).deleted_count
        users_deleted = db.users.delete_many({"_id": {"$in": user_ids}}).deleted_count

        logger.info(
            "Test cleanup completed: users=%s, notes=%s, labels=%s",
            users_deleted,
            notes_deleted,
            labels_deleted,
        )
    except Exception as error:
        logger.warning("Test cleanup skipped due to DB error: %s", error)
    finally:
        if client:
            client.close()


# ==================== HOOKS ====================
def pytest_configure(config):
    """Configure pytest with custom settings."""
    logger.info(f"Pytest configuration loaded: {config.inifile}")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on directory structure."""
    for item in items:
        # Mark by directory
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        
        # Mark by test name prefix
        if "auth" in item.name:
            item.add_marker(pytest.mark.auth)
        if "note" in item.name or "notes" in item.name:
            item.add_marker(pytest.mark.notes)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Create test report with additional info."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.failed and hasattr(item, "funcargs"):
        # Store failure info for later use
        rep.user_properties.append(("failed", True))
