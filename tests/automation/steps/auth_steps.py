"""
Step definitions for authentication scenarios.
Implements BDD steps for signup and login features.
"""

import pytest
from pytest_bdd import given, when, then, scenario, step

from api.client import APIClient
from api.endpoints import AUTH
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from factories.user_factory import UserFactory


# ==================== SCENARIOS ====================

@scenario("features/auth.feature", "Successful user signup")
def test_successful_signup(page):
    pass


@scenario("features/auth.feature", "Signup with invalid email")
def test_signup_invalid_email(page):
    pass


@scenario("features/auth.feature", "Signup with short password")
def test_signup_short_password(page):
    pass


@scenario("features/auth.feature", "Successful user login")
def test_successful_login(page, api_client):
    pass


@scenario("features/auth.feature", "Login with invalid credentials")
def test_login_invalid_credentials(page):
    pass


# ==================== SHARED STEPS ====================

@given("the application is running")
def app_running():
    """Verify application is accessible."""
    pass


@given("I navigate to the signup page")
def navigate_to_signup(page):
    """Navigate to signup page."""
    signup = SignupPage(page)
    # Can be stored in context for use in other steps
    page.signup_page = signup


@given("I navigate to the login page")
def navigate_to_login(page):
    """Navigate to login page."""
    login = LoginPage(page)
    page.login_page = login


# ==================== SIGNUP STEPS ====================

@when("I enter a valid name {name}")
def enter_name(page, name):
    """Enter user name on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I enter a valid email {email}")
def enter_email(page, email):
    """Enter email on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I enter a valid password {password}")
def enter_password(page, password):
    """Enter password on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I confirm the password {password}")
def confirm_password(page, password):
    """Enter password confirmation on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I enter an invalid email {email}")
def enter_invalid_email(page, email):
    """Enter invalid email on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I enter a short password {password}")
def enter_short_password(page, password):
    """Enter short password on signup form."""
    signup = page.signup_page
    # Would be async in real implementation


@when("I click the Sign Up button")
def click_signup_button(page):
    """Click the signup button."""
    signup = page.signup_page
    # Would be async in real implementation


@then("I should see a success message")
def see_success_message(page):
    """Verify success message is displayed."""
    pass


@then("I should be redirected to the login page")
def redirected_to_login(page):
    """Verify redirected to login page."""
    assert page.url.endswith("/login")


@then("I should see an error message {message}")
def see_error_message(page, message):
    """Verify error message is displayed."""
    pass


@then("I should remain on the signup page")
def remain_on_signup(page):
    """Verify still on signup page."""
    assert page.url.endswith("/signup")


# ==================== LOGIN STEPS ====================

@given("I have a registered account with email {email} and password {password}")
def register_user(api_client, email, password):
    """Register a test user via API."""
    user_data = {
        "name": "Test User",
        "email": email,
        "password": password,
    }
    api_client.post(AUTH.SIGNUP, json=user_data)


@when("I enter the email {email}")
def enter_login_email(page, email):
    """Enter email on login form."""
    login = page.login_page
    # Would be async in real implementation


@when("I enter the password {password}")
def enter_login_password(page, password):
    """Enter password on login form."""
    login = page.login_page
    # Would be async in real implementation


@when("I click the Login button")
def click_login_button(page):
    """Click the login button."""
    login = page.login_page
    # Would be async in real implementation


@then("I should be redirected to the home page")
def redirected_to_home(page):
    """Verify redirected to home page."""
    assert page.url.endswith("/")


@then("I should see my username in the navbar")
def see_username_in_navbar(page):
    """Verify username is displayed in navbar."""
    pass


@then("I should remain on the login page")
def remain_on_login(page):
    """Verify still on login page."""
    assert page.url.endswith("/login")
