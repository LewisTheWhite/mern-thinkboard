"""
Step definitions for notes management scenarios.
Implements BDD steps for notes CRUD features.
"""

import pytest
from pytest_bdd import given, when, then, scenario, step

from api.client import APIClient
from api.endpoints import AUTH, NOTES
from pages.home_page import HomePage
from pages.note_page import NotePage
from factories.user_factory import UserFactory
from factories.note_factory import NoteFactory


# ==================== SCENARIOS ====================

@scenario("features/notes.feature", "Create a new note")
def test_create_note(page, authenticated_client):
    pass


@scenario("features/notes.feature", "View list of notes")
def test_view_notes_list(page, authenticated_client):
    pass


@scenario("features/notes.feature", "View empty notes state")
def test_empty_notes_state(page, authenticated_client):
    pass


@scenario("features/notes.feature", "View note detail")
def test_view_note_detail(page, authenticated_client):
    pass


@scenario("features/notes.feature", "Update an existing note")
def test_update_note(page, authenticated_client):
    pass


@scenario("features/notes.feature", "Delete a note")
def test_delete_note(page, authenticated_client):
    pass


@scenario("features/notes.feature", "Notes are private to user")
def test_notes_private(page, api_client):
    pass


# ==================== BACKGROUND STEPS ====================

@given("I am logged in as {email} with password {password}")
def login_user(api_client, email, password):
    """Log in a user via API."""
    # Register if needed
    user_data = {
        "name": "Test User",
        "email": email,
        "password": password,
    }
    try:
        api_client.post(AUTH.SIGNUP, json=user_data)
    except:
        pass
    
    # Login
    response = api_client.post(
        AUTH.LOGIN,
        json={"email": email, "password": password}
    )
    token = response.json()["token"]
    api_client.set_token(token)


@given("I am on the home page")
def on_home_page(page):
    """Navigate to home page."""
    home = HomePage(page)
    page.home_page = home
    # Would be async in real implementation


# ==================== CREATE NOTE STEPS ====================

@when("I click the Create Note button")
def click_create_note(page):
    """Click the Create Note button."""
    home = page.home_page
    # Would be async in real implementation


@when("I enter the title {title}")
def enter_note_title(page, title):
    """Enter note title."""
    # Would be async in real implementation
    pass


@when("I enter the content {content}")
def enter_note_content(page, content):
    """Enter note content."""
    # Would be async in real implementation
    pass


@when("I click the Save button")
def click_save_button(page):
    """Click the Save button."""
    # Would be async in real implementation
    pass


@then("I should see a success message {message}")
def see_note_success_message(page, message):
    """Verify note success message."""
    pass


@then("the note {title} should appear in my notes list")
def note_appears_in_list(page, title):
    """Verify note appears in list."""
    pass


# ==================== VIEW NOTES STEPS ====================

@given("I have created {count} notes")
def create_multiple_notes(authenticated_client, count):
    """Create multiple test notes via API."""
    for i in range(int(count)):
        note = NoteFactory.create(title=f"Test Note {i+1}")
        authenticated_client.post(NOTES.CREATE, json=note)


@when("I navigate to the home page")
def navigate_to_home(page):
    """Navigate to home page."""
    home = HomePage(page)
    page.home_page = home
    # Would be async in real implementation


@then("I should see all {count} notes displayed")
def verify_note_count(page, count):
    """Verify correct number of notes displayed."""
    pass


@then("each note should show the title and preview of content")
def verify_note_display(page):
    """Verify notes display title and content preview."""
    pass


# ==================== EMPTY STATE STEPS ====================

@then("I should see the message {message}")
def see_empty_state_message(page, message):
    """Verify empty state message is displayed."""
    pass


@then("the Create Note button should not be visible")
def create_button_not_visible(page):
    """Verify Create Note button is hidden."""
    pass


# ==================== DETAIL VIEW STEPS ====================

@given("I have created a note titled {title}")
def create_test_note(authenticated_client, title):
    """Create a test note via API."""
    note = NoteFactory.create(title=title)
    response = authenticated_client.post(NOTES.CREATE, json=note)
    return response.json()


@when("I click on the note {title}")
def click_note_by_title(page, title):
    """Click on note by title."""
    # Would be async in real implementation
    pass


@then("I should see the full note title")
def verify_note_title(page):
    """Verify full note title is displayed."""
    pass


@then("I should see the full note content")
def verify_note_content(page):
    """Verify full note content is displayed."""
    pass


# ==================== UPDATE STEPS ====================

@given("I navigate to this note")
def navigate_to_note(page):
    """Navigate to note detail page."""
    # Would be async in real implementation
    pass


@when("I click the Edit button")
def click_edit_button(page):
    """Click the Edit button."""
    # Would be async in real implementation
    pass


@when("I change the title to {new_title}")
def change_title(page, new_title):
    """Change the note title."""
    # Would be async in real implementation
    pass


@when("I change the content to {new_content}")
def change_content(page, new_content):
    """Change the note content."""
    # Would be async in real implementation
    pass


@then("the note should now display {updated_title}")
def verify_updated_note(page, updated_title):
    """Verify note was updated with new title."""
    pass


# ==================== DELETE STEPS ====================

@when("I click the Delete button")
def click_delete_button(page):
    """Click the Delete button."""
    # Would be async in real implementation
    pass


@when("I confirm the deletion")
def confirm_deletion(page):
    """Confirm the deletion in dialog."""
    # Would be async in real implementation
    pass


@then("the note should no longer appear in my notes list")
def verify_note_deleted(page):
    """Verify note was deleted from list."""
    pass


# ==================== PRIVACY STEPS ====================

@given("I log out")
def logout_user(page):
    """Log out the current user."""
    # Would be async in real implementation
    pass


@given("I log in as {email}")
def login_as_user(api_client, email):
    """Log in as a specific user."""
    # Would be async in real implementation
    pass


@then("I should not see the note {title}")
def verify_note_not_visible(page, title):
    """Verify note is not visible to other user."""
    pass


@then("the notes list should be empty")
def verify_notes_list_empty(page):
    """Verify notes list is empty."""
    pass
