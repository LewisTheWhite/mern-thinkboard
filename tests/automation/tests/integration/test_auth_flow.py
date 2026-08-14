"""
Integration tests for complete authentication and notes workflows.
Tests user journeys involving multiple API calls.
"""

import pytest

from api.client import APIClient
from api.endpoints import AUTH, NOTES
from factories.user_factory import UserFactory
from factories.note_factory import NoteFactory


class TestSignupLoginFlow:
    """Integration tests for signup and login."""
    
    def test_signup_then_login(self, api_client: APIClient, test_user_data):
        """Test complete signup then login flow."""
        # Step 1: Signup
        signup_response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        assert signup_response.status_code == 201
        signup_data = signup_response.json()
        signup_token = signup_data["token"]
        
        # Step 2: Login with same credentials
        login_response = api_client.post(
            AUTH.LOGIN,
            json={"email": test_user_data["email"], "password": test_user_data["password"]}
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        login_token = login_data["token"]
        
        # Both should return valid tokens
        assert signup_token
        assert login_token
    
    def test_signup_login_access_me(self, api_client: APIClient, test_user_data):
        """Test signup, login, and access me endpoint."""
        # Signup
        signup_response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        token = signup_response.json()["token"]
        
        # Use token to access me endpoint
        api_client.set_token(token)
        me_response = api_client.get(AUTH.ME)
        
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["email"] == test_user_data["email"]


class TestAuthenticatedNoteFlow:
    """Integration tests for authenticated notes operations."""
    
    def test_signup_create_list_notes(self, api_client: APIClient, test_user_data):
        """Test signup, then create and list notes."""
        # Signup
        signup_response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        token = signup_response.json()["token"]
        api_client.set_token(token)
        
        # Verify empty list initially
        list_response = api_client.get(NOTES.LIST)
        assert list_response.status_code == 200
        assert len(list_response.json()) == 0
        
        # Create multiple notes
        note1_data = NoteFactory.create()
        note1_response = api_client.post(NOTES.CREATE, json=note1_data)
        assert note1_response.status_code == 201
        
        note2_data = NoteFactory.create()
        note2_response = api_client.post(NOTES.CREATE, json=note2_data)
        assert note2_response.status_code == 201
        
        # List should now have 2 notes
        list_response = api_client.get(NOTES.LIST)
        assert len(list_response.json()) == 2
    
    def test_signup_create_update_delete_note(self, api_client: APIClient, test_user_data):
        """Test complete note lifecycle: create, update, delete."""
        # Signup
        signup_response = api_client.post(AUTH.SIGNUP, json=test_user_data)
        token = signup_response.json()["token"]
        api_client.set_token(token)
        
        # Create note
        note_data = NoteFactory.create()
        create_response = api_client.post(NOTES.CREATE, json=note_data)
        assert create_response.status_code == 201
        note_id = create_response.json()["_id"]
        
        # Get note
        get_response = api_client.get(NOTES.GET(note_id))
        assert get_response.status_code == 200
        assert get_response.json()["title"] == note_data["title"]
        
        # Update note
        update_data = {"title": "Updated Title", "content": "Updated Content"}
        update_response = api_client.put(NOTES.UPDATE(note_id), json=update_data)
        assert update_response.status_code == 200
        updated_note = update_response.json()
        assert updated_note["title"] == "Updated Title"
        
        # Delete note
        delete_response = api_client.delete(NOTES.DELETE(note_id))
        assert delete_response.status_code == 200
        
        # Verify deleted
        get_response = api_client.get(NOTES.GET(note_id))
        assert get_response.status_code == 404
    
    def test_multiple_users_note_isolation(self, api_client: APIClient):
        """Test that different users can't see each other's notes."""
        # Create and login first user
        user1_data = UserFactory.create()
        user1_signup = api_client.post(AUTH.SIGNUP, json=user1_data)
        user1_token = user1_signup.json()["token"]
        api_client.set_token(user1_token)
        
        # User 1 creates a note
        note1_data = NoteFactory.create(title="User 1 Note")
        note1_response = api_client.post(NOTES.CREATE, json=note1_data)
        note1_id = note1_response.json()["_id"]
        
        # Logout user 1
        api_client.set_token(None)
        
        # Create and login second user
        user2_data = UserFactory.create()
        user2_signup = api_client.post(AUTH.SIGNUP, json=user2_data)
        user2_token = user2_signup.json()["token"]
        api_client.set_token(user2_token)
        
        # User 2 lists notes - should be empty
        list_response = api_client.get(NOTES.LIST)
        assert len(list_response.json()) == 0
        
        # User 2 tries to get user 1's note - should fail
        get_response = api_client.get(NOTES.GET(note1_id))
        assert get_response.status_code == 404  # or 403 Forbidden
