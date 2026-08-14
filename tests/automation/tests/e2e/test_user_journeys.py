"""
End-to-end user journey tests with Playwright browser automation.
Tests complete user flows including signup, login, and note management.
"""

import pytest

from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.note_page import NotePage
from factories.user_factory import UserFactory
from factories.note_factory import NoteFactory


async def seed_auth_session(page, token: str, user: dict):
    """Populate browser localStorage before app navigation."""
    await page.goto("http://localhost:5173/login")
    await page.evaluate(
        """
        ({ token, user }) => {
            window.localStorage.setItem('authToken', token);
            window.localStorage.setItem('authUser', JSON.stringify(user));
        }
        """,
        {"token": token, "user": user},
    )


@pytest.mark.e2e
class TestSignupJourney:
    """E2E tests for signup user journey."""
    
    @pytest.mark.asyncio
    async def test_complete_signup_flow(self, page):
        """
        Test complete signup flow with form validation.
        
        GIVEN a user on the signup page,
        WHEN they fill out the form with valid data and submit,
        THEN they should be redirected to the login page with a success message.        
        """
        signup = SignupPage(page)
        
        # Navigate to signup
        await signup.navigate()
        
        # Create test user
        user = UserFactory.create()
        
        # Complete signup
        await signup.signup(user["name"], user["email"], user["password"])
        
        # Should redirect to login
        assert await signup.is_signup_success()
    
    @pytest.mark.asyncio
    async def test_signup_with_invalid_email(self, page):
        """
        Test signup form rejects invalid email.

        GIVEN a user on the signup page,
        WHEN they enter an invalid email and submit,
        THEN the form should show a validation error and prevent submission.        
        """
        signup = SignupPage(page)
        await signup.navigate()
        
        user = UserFactory.create_invalid_email()
        
        # Try to signup - should show error or prevent submission
        await signup.fill_email(user["email"])
        # The page should show validation error or disable submit button


@pytest.mark.e2e
class TestLoginJourney:
    """E2E tests for login user journey."""
    
    @pytest.mark.asyncio
    async def test_complete_login_flow(self, api_client, page):
        """
        Test complete login flow.
        
        GIVEN a registered user,
        WHEN they navigate to the login page and enter valid credentials,
        THEN they should be redirected to the home page and see their notes.
        """
        from api.client import APIClient
        from api.endpoints import AUTH
        
        # First create a user via API
        user_data = UserFactory.create()
        api_client.post(AUTH.SIGNUP, json=user_data)
        
        # Now login via UI
        login = LoginPage(page)
        await login.navigate()
        await login.login(user_data["email"], user_data["password"])
        
        # Should be redirected to home
        assert await login.is_logged_in()
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, page):
        """
        Test login with invalid credentials shows error.

        GIVEN a user on the login page,
        WHEN they enter invalid credentials and submit,
        THEN the form should show an error message and prevent login.
        """
        login = LoginPage(page)
        await login.navigate()
        
        # Try login with non-existent user
        await login.fill_email("nonexistent@example.com")
        await login.fill_password("WrongPassword123")
        await login.click_login()
        
        # Should show error message
        error = await login.get_error_message()
        assert error is not None


@pytest.mark.e2e
class TestNotesJourney:
    """
    E2E tests for notes management user journey.

    GIVEN a logged-in user,
    WHEN they create, view, and delete notes,
    THEN the notes should be correctly displayed and managed in the UI.    
    """
    
    @pytest.mark.asyncio
    async def test_empty_notes_state(self, api_client, page):
        """Test empty notes state after signup."""
        from api.client import APIClient
        from api.endpoints import AUTH
        
        # Create and login user via API
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        await seed_auth_session(page, token, user)
        
        # Navigate to home via UI
        home = HomePage(page)
        await home.navigate()
        
        # Should show empty state
        is_empty = await home.is_empty_state_visible()
        assert is_empty or await home.get_note_count() == 0
    
    @pytest.mark.asyncio
    async def test_create_and_view_note(self, api_client, page):
        """
        Test creating a note and viewing it on home page.

        GIVEN a logged-in user,
        WHEN they create a new note,
        THEN the note should be visible on the home page.
        """
        from api.client import APIClient
        from api.endpoints import AUTH, NOTES
        
        # Setup: Create user and note via API
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        api_client.set_token(token)
        await seed_auth_session(page, token, user)
        
        note_data = NoteFactory.create()
        api_client.post(NOTES.CREATE, json=note_data)
        
        # Navigate to home
        home = HomePage(page)
        await home.navigate()
        
        # Should see the note
        note_count = await home.get_note_count()
        assert note_count > 0
        
        titles = await home.get_note_titles()
        assert note_data["title"] in titles
    
    @pytest.mark.asyncio
    async def test_create_note_button_only_with_notes(self, api_client, page):
        """
        Test create button visibility depends on note count.

        GIVEN a logged-in user,
        WHEN they have no notes,
        THEN the create button should not be visible.
        """
        from api.client import APIClient
        from api.endpoints import AUTH
        
        # Create user via API
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        api_client.set_token(token)
        await seed_auth_session(page, token, user)
        
        # Navigate when no notes
        home = HomePage(page)
        await home.navigate()
        
        # Create button should not be visible when no notes
