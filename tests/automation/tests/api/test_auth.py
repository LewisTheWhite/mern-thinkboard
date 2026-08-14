"""
API tests for authentication endpoints.
Tests signup, login, and user profile endpoints.
"""

import pytest

from api.client import APIClient
from api.endpoints import AUTH
from factories.user_factory import UserFactory
from factories.note_factory import NoteFactory

class TestSignup:
    """Signup endpoint tests."""
    
    def test_signup_success(self, api_client: APIClient, test_user_data):
        """Test successful user signup."""
        response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == test_user_data["email"]
    
    def test_signup_invalid_email(self, api_client: APIClient):
        """Test signup with invalid email format."""
        user = UserFactory.create_invalid_email()
        response = api_client.post(AUTH.SIGNUP, json=user)
        
        assert response.status_code != 201
        # Could be 400 or 422 depending on implementation
    
    def test_signup_duplicate_email(self, api_client: APIClient, test_user_data):
        """Test signup with already registered email."""
        # First signup
        api_client.post(AUTH.SIGNUP, json=test_user_data)
        
        # Try to signup again with same email
        response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        
        assert response.status_code == 409
    
    def test_signup_short_password(self, api_client: APIClient):
        """Test signup with password shorter than 8 characters."""
        user = UserFactory.create_invalid_password()
        response = api_client.post(AUTH.SIGNUP, json=user)
        
        assert response.status_code != 201
    
    def test_signup_missing_fields(self, api_client: APIClient):
        """Test signup with missing required fields."""
        user = {"email": "test@example.com"}  # missing name and password
        response = api_client.post(AUTH.SIGNUP, json=user)
        
        assert response.status_code == 400


class TestLogin:
    """Login endpoint tests."""
    
    def test_login_success(self, api_client: APIClient, registered_user):
        """Test successful login."""
        user = registered_user["user"]
        response = api_client.post(
            AUTH.LOGIN,
            json={"email": user["email"], "password": user["password"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
    
    def test_login_invalid_email(self, api_client: APIClient):
        """Test login with non-existent email."""
        response = api_client.post(
            AUTH.LOGIN,
            json={"email": "nonexistent@example.com", "password": "AnyPassword123"}
        )
        
        assert response.status_code == 401
    
    def test_login_invalid_password(self, api_client: APIClient, registered_user):
        """Test login with wrong password."""
        user = registered_user["user"]
        response = api_client.post(
            AUTH.LOGIN,
            json={"email": user["email"], "password": "WrongPassword123"}
        )
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, api_client: APIClient):
        """Test login with missing email or password."""
        response = api_client.post(AUTH.LOGIN, json={"email": "test@example.com"})
        assert response.status_code == 400
        
        response = api_client.post(AUTH.LOGIN, json={"password": "Password123"})
        assert response.status_code == 400


class TestMeEndpoint:
    """User profile (me) endpoint tests."""
    
    def test_me_authenticated(self, authenticated_client: APIClient, registered_user):
        """Test getting authenticated user profile."""
        response = authenticated_client.get(AUTH.ME)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == registered_user["user"]["email"]
        assert "password" not in data  # Password should not be exposed
    
    def test_me_unauthenticated(self, api_client: APIClient):
        """Test me endpoint without authentication."""
        response = api_client.get(AUTH.ME)
        
        assert response.status_code == 401
    
    def test_me_invalid_token(self, api_client: APIClient):
        """Test me endpoint with invalid token."""
        api_client.set_token("invalid.token.here")
        response = api_client.get(AUTH.ME)
        
        assert response.status_code == 401
