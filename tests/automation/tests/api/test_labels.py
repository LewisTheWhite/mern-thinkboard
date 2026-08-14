"""
API tests for label endpoints.
Tests listing, creating, and deleting labels.
"""

from uuid import uuid4

from api.client import APIClient
from api.endpoints import LABELS, NOTES
from factories.note_factory import NoteFactory


def build_label_payload(name: str | None = None, color: str = "#10b981"):
    """Build unique label payloads for tests."""
    return {
        "name": name or f"Label-{uuid4().hex[:8]}",
        "color": color,
    }


class TestLabelsAPI:
    """Tests for labels API endpoints."""

    def test_create_label_success(self, authenticated_client: APIClient):
        """Test creating a custom label."""
        payload = build_label_payload()

        response = authenticated_client.post(LABELS.CREATE, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["color"] == payload["color"]
        assert data["isDefault"] is False
        assert "_id" in data

    def test_get_labels_includes_defaults_and_custom_labels(self, authenticated_client: APIClient):
        """Test label listing returns both default and user-created labels."""
        custom_label = authenticated_client.post(LABELS.CREATE, json=build_label_payload()).json()

        response = authenticated_client.get(LABELS.LIST)

        assert response.status_code == 200
        labels = response.json()
        assert any(label["isDefault"] for label in labels)
        assert any(label["_id"] == custom_label["_id"] for label in labels)

    def test_create_label_duplicate_name_conflicts(self, authenticated_client: APIClient):
        """Test duplicate custom label names are rejected."""
        payload = build_label_payload(name=f"Duplicate-{uuid4().hex[:6]}")

        first_response = authenticated_client.post(LABELS.CREATE, json=payload)
        duplicate_response = authenticated_client.post(LABELS.CREATE, json=payload)

        assert first_response.status_code == 201
        assert duplicate_response.status_code == 409

    def test_delete_default_label_forbidden(self, authenticated_client: APIClient):
        """Test built-in labels cannot be deleted."""
        labels_response = authenticated_client.get(LABELS.LIST)
        default_label = next(label for label in labels_response.json() if label["isDefault"])

        response = authenticated_client.delete(LABELS.DELETE(default_label["_id"]))

        assert response.status_code == 403

    def test_delete_custom_label_removes_it_from_notes(self, authenticated_client: APIClient):
        """Test deleting a custom label also removes it from the user's notes."""
        label = authenticated_client.post(LABELS.CREATE, json=build_label_payload()).json()
        note = authenticated_client.post(
            NOTES.CREATE,
            json={**NoteFactory.create(), "labels": [label["_id"]]},
        ).json()

        delete_response = authenticated_client.delete(LABELS.DELETE(label["_id"]))
        note_response = authenticated_client.get(NOTES.GET(note["_id"]))

        assert delete_response.status_code == 200
        assert note_response.status_code == 200
        assert note_response.json()["labels"] == []