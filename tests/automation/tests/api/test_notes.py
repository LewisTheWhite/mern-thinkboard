"""
API tests for notes endpoints.
Tests CRUD operations on notes.
"""

import pytest

from api.client import APIClient
from api.endpoints import NOTES
from factories.note_factory import NoteFactory


class TestNotesAPI:
    """Tests for notes API endpoints."""
    
    def test_create_note_success(self, authenticated_client: APIClient):
        """Test creating a new note."""
        note_data = NoteFactory.create()
        response = authenticated_client.post(NOTES.CREATE, json=note_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        assert "_id" in data
    
    def test_list_notes_empty(self, authenticated_client: APIClient):
        """Test listing notes when empty."""
        response = authenticated_client.get(NOTES.LIST)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_list_notes_with_data(self, authenticated_client: APIClient):
        """Test listing notes with existing notes."""
        # Create 3 notes
        for _ in range(3):
            note = NoteFactory.create()
            authenticated_client.post(NOTES.CREATE, json=note)
        
        response = authenticated_client.get(NOTES.LIST)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_note_success(self, authenticated_client: APIClient):
        """Test getting a specific note."""
        # Create a note first
        note_data = NoteFactory.create()
        create_response = authenticated_client.post(NOTES.CREATE, json=note_data)
        note_id = create_response.json()["_id"]
        
        # Get the note
        response = authenticated_client.get(NOTES.GET(note_id))
        
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == note_id
        assert data["title"] == note_data["title"]
    
    def test_get_note_not_found(self, authenticated_client: APIClient):
        """Test getting a non-existent note."""
        fake_id = "507f1f77bcf86cd799439011"  # Valid MongoDB ID format
        response = authenticated_client.get(NOTES.GET(fake_id))
        
        assert response.status_code == 404
    
    def test_update_note_success(self, authenticated_client: APIClient):
        """Test updating a note."""
        # Create a note
        note_data = NoteFactory.create()
        create_response = authenticated_client.post(NOTES.CREATE, json=note_data)
        note_id = create_response.json()["_id"]
        
        # Update the note
        updated_data = {"title": "Updated Title", "content": "Updated content"}
        response = authenticated_client.put(NOTES.UPDATE(note_id), json=updated_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
    
    def test_delete_note_success(self, authenticated_client: APIClient):
        """Test deleting a note."""
        # Create a note
        note_data = NoteFactory.create()
        create_response = authenticated_client.post(NOTES.CREATE, json=note_data)
        note_id = create_response.json()["_id"]
        
        # Delete the note
        response = authenticated_client.delete(NOTES.DELETE(note_id))
        
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = authenticated_client.get(NOTES.GET(note_id))
        assert get_response.status_code == 404
    
    def test_create_note_unauthenticated(self, api_client: APIClient):
        """Test creating note without authentication."""
        note_data = NoteFactory.create()
        response = api_client.post(NOTES.CREATE, json=note_data)
        
        assert response.status_code == 401
    
    def test_list_notes_unauthenticated(self, api_client: APIClient):
        """Test listing notes without authentication."""
        response = api_client.get(NOTES.LIST)
        
        assert response.status_code == 401
