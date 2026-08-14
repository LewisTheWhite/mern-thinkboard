"""
API tests for note filtering behavior.
Tests title, label, and date filters on the notes listing endpoint.
"""

from datetime import date
from uuid import uuid4

from api.client import APIClient
from api.endpoints import LABELS, NOTES
from factories.note_factory import NoteFactory


def create_label(authenticated_client: APIClient, name: str, color: str = "#3b82f6"):
    """Create a label and return its API payload."""
    response = authenticated_client.post(LABELS.CREATE, json={"name": name, "color": color})
    assert response.status_code == 201
    return response.json()


class TestNoteFiltersAPI:
    """Tests for server-side note filtering."""

    def test_filter_notes_by_title_returns_matching_notes(self, authenticated_client: APIClient):
        """Test title filtering only returns matching notes."""
        target_title = f"Alpha Focus {uuid4().hex[:6]}"
        other_title = f"Beta Archive {uuid4().hex[:6]}"

        authenticated_client.post(NOTES.CREATE, json=NoteFactory.create(title=target_title))
        authenticated_client.post(NOTES.CREATE, json=NoteFactory.create(title=other_title))

        response = authenticated_client.get(NOTES.LIST, params={"title": "Alpha Focus"})

        assert response.status_code == 200
        titles = [note["title"] for note in response.json()]
        assert target_title in titles
        assert other_title not in titles

    def test_filter_notes_by_label_returns_only_matching_notes(self, authenticated_client: APIClient):
        """Test label filtering only returns notes with the selected label."""
        urgent_label = create_label(authenticated_client, f"Urgent-{uuid4().hex[:6]}", "#ef4444")
        archive_label = create_label(authenticated_client, f"Archive-{uuid4().hex[:6]}", "#64748b")

        matching_note = authenticated_client.post(
            NOTES.CREATE,
            json={**NoteFactory.create(title=f"Urgent task {uuid4().hex[:4]}"), "labels": [urgent_label["_id"]]},
        ).json()
        other_note = authenticated_client.post(
            NOTES.CREATE,
            json={**NoteFactory.create(title=f"Archive task {uuid4().hex[:4]}"), "labels": [archive_label["_id"]]},
        ).json()

        response = authenticated_client.get(NOTES.LIST, params={"labels": urgent_label["_id"]})

        assert response.status_code == 200
        notes = response.json()
        note_ids = [note["_id"] for note in notes]
        assert matching_note["_id"] in note_ids
        assert other_note["_id"] not in note_ids
        assert all(any(label["_id"] == urgent_label["_id"] for label in note["labels"]) for note in notes)

    def test_filter_notes_by_date_range_returns_notes_for_today(self, authenticated_client: APIClient):
        """Test date range filtering includes notes created on the selected date."""
        created_note = authenticated_client.post(
            NOTES.CREATE,
            json=NoteFactory.create(title=f"Today note {uuid4().hex[:6]}"),
        ).json()
        today = date.today().isoformat()

        response = authenticated_client.get(
            NOTES.LIST,
            params={"dateFrom": today, "dateTo": today},
        )

        assert response.status_code == 200
        note_ids = [note["_id"] for note in response.json()]
        assert created_note["_id"] in note_ids