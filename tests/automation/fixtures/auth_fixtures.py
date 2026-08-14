"""
Authentication fixtures for testing auth flows.
"""

import pytest

from api.client import APIClient
from api.endpoints import AUTH
from factories.user_factory import UserFactory
from settings import config


@pytest.fixture
def registered_user(api_client: APIClient, test_user_data):
    """
    Fixture that creates and registers a test user.
    Returns user data and auth token.
    """
    response = api_client.post(AUTH.SIGNUP, json=test_user_data)
    assert response.status_code == 201, f"Signup failed: {response.text}"
    
    data = response.json()
    return {
        "user": test_user_data,
        "token": data.get("token"),
        "user_id": data.get("user", {}).get("_id"),
    }


@pytest.fixture
def authenticated_client(api_client: APIClient, registered_user):
    """
    Fixture that provides an authenticated API client.
    Uses registered_user fixture to obtain token.
    """
    api_client.set_token(registered_user["token"])
    return api_client
