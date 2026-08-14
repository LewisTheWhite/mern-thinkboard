"""
End-to-end tests for label management and note filtering.
"""

from uuid import uuid4

import pytest

from api.endpoints import AUTH, LABELS, NOTES
from factories.note_factory import NoteFactory
from factories.user_factory import UserFactory
from pages.home_page import HomePage


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
class TestLabelsAndFiltersJourney:
    """UI coverage for labels modal and note filters."""

    @pytest.mark.asyncio
    async def test_manage_labels_modal_can_create_custom_label(self, api_client, page):
        """Test a signed-in user can create a custom label from the UI."""
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        await seed_auth_session(page, token, user)

        home = HomePage(page)
        await home.navigate()
        await home.open_labels_modal()

        label_name = f"UI Label {uuid4().hex[:6]}"
        await home.create_label(label_name, "#22c55e")

        assert await home.is_label_visible_in_modal(label_name)

    @pytest.mark.asyncio
    async def test_filter_notes_by_title_from_sidebar(self, api_client, page):
        """Test the title filter narrows visible notes."""
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        api_client.set_token(token)
        await seed_auth_session(page, token, user)

        matching_title = f"Alpha Target {uuid4().hex[:6]}"
        other_title = f"Beta Spare {uuid4().hex[:6]}"
        api_client.post(NOTES.CREATE, json=NoteFactory.create(title=matching_title))
        api_client.post(NOTES.CREATE, json=NoteFactory.create(title=other_title))

        home = HomePage(page)
        await home.navigate()
        await home.open_filters()
        await home.filter_by_title("Alpha Target")

        titles = [title.strip() for title in await home.get_note_titles()]
        assert matching_title in titles
        assert other_title not in titles

        await home.clear_filters()
        cleared_titles = [title.strip() for title in await home.get_note_titles()]
        assert matching_title in cleared_titles
        assert other_title in cleared_titles

    @pytest.mark.asyncio
    async def test_filter_notes_by_label_from_sidebar(self, api_client, page):
        """Test the label filter only shows notes tagged with the chosen label."""
        user_data = UserFactory.create()
        response = api_client.post(AUTH.SIGNUP, json=user_data)
        token = response.json()["token"]
        user = response.json()["user"]
        api_client.set_token(token)
        await seed_auth_session(page, token, user)

        focus_label_name = f"Focus {uuid4().hex[:6]}"
        other_label_name = f"Later {uuid4().hex[:6]}"
        focus_label = api_client.post(LABELS.CREATE, json={"name": focus_label_name, "color": "#8b5cf6"}).json()
        other_label = api_client.post(LABELS.CREATE, json={"name": other_label_name, "color": "#f59e0b"}).json()

        focus_title = f"Focus note {uuid4().hex[:6]}"
        other_title = f"Later note {uuid4().hex[:6]}"
        api_client.post(NOTES.CREATE, json={**NoteFactory.create(title=focus_title), "labels": [focus_label["_id"]]})
        api_client.post(NOTES.CREATE, json={**NoteFactory.create(title=other_title), "labels": [other_label["_id"]]})

        home = HomePage(page)
        await home.navigate()
        await home.open_filters()
        await home.toggle_label_filter(focus_label_name)

        titles = [title.strip() for title in await home.get_note_titles()]
        assert focus_title in titles
        assert other_title not in titles