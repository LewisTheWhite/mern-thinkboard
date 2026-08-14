"""
Home page object model.
"""

import logging

logger = logging.getLogger(__name__)


def _is_notes_response(response):
    return response.request.method == "GET" and "/api/notes" in response.url and response.status == 200


class HomePage:
    """Page object for home/notes listing page."""
    
    def __init__(self, page):
        """Initialize home page."""
        self.page = page
        self.base_url = "http://localhost:5173"
        
        # Selectors
        self.create_note_button = 'a:has-text("New Note")'
        self.note_cards = 'a[href^="/note/"]'
        self.notes_not_found = 'text=No Notes yet'
        self.logout_button = 'button:has-text("Logout")'
        self.loading_message = 'text=Loading notes...'
        self.note_titles = 'a[href^="/note/"] .card-title'
        self.labels_button = 'button:has-text("Labels")'
        self.labels_modal = '.modal-box'
        self.new_label_input = 'input[placeholder="Label name"]'
        self.label_color_input = 'input[type="color"]'
        self.create_label_button = '.modal-box button[type="submit"]'
        self.filters_button = 'button:has-text("Filters"), button:has-text("Hide Filters")'
        self.filter_sidebar = 'aside'
        self.title_filter_input = 'input[placeholder="Search notes..."]'
        self.clear_filters_button = 'aside button:has-text("Clear")'
        self.no_filter_results = 'text=No notes match your filters.'
    
    async def navigate(self):
        """Navigate to home page."""
        logger.info("Navigating to home page")
        await self.page.goto(f"{self.base_url}/")
        await self.page.wait_for_url(f"{self.base_url}/", timeout=5000)
        await self.wait_until_loaded()

    async def wait_until_loaded(self):
        """Wait for notes page to finish initial loading."""
        await self.page.wait_for_load_state("networkidle")
        try:
            await self.page.wait_for_selector(self.loading_message, state="hidden", timeout=10000)
        except:
            pass
    
    async def click_create_note(self):
        """Click create note button."""
        logger.info("Clicking create note button")
        await self.page.click(self.create_note_button)
        await self.page.wait_for_url(f"{self.base_url}/create", timeout=5000)
    
    async def is_empty_state_visible(self) -> bool:
        """Check if empty state message is visible."""
        await self.wait_until_loaded()
        try:
            await self.page.wait_for_selector(self.notes_not_found, timeout=2000)
            return True
        except:
            return False
    
    async def get_note_count(self) -> int:
        """Get number of note cards visible."""
        await self.wait_until_loaded()
        try:
            await self.page.wait_for_selector(self.note_cards, timeout=3000)
        except:
            pass
        cards = await self.page.query_selector_all(self.note_cards)
        return len(cards)
    
    async def get_note_titles(self) -> list:
        """Get list of note titles visible."""
        await self.wait_until_loaded()
        try:
            await self.page.wait_for_selector(self.note_titles, timeout=3000)
        except:
            pass
        titles = await self.page.query_selector_all(self.note_titles)
        return [await title.text_content() for title in titles]
    
    async def click_note_by_title(self, title: str):
        """Click on a note by its title."""
        logger.info(f"Clicking on note: {title}")
        await self.page.click(f'text={title}')

    async def open_labels_modal(self):
        """Open label management modal."""
        logger.info("Opening labels modal")
        await self.page.click(self.labels_button)
        await self.page.wait_for_selector(self.labels_modal, timeout=5000)

    async def create_label(self, name: str, color: str = "#10b981"):
        """Create a label from the labels modal."""
        logger.info(f"Creating label: {name}")
        await self.page.fill(self.new_label_input, name)
        await self.page.fill(self.label_color_input, color)
        await self.page.click(self.create_label_button)
        await self.page.locator(self.labels_modal).locator(f'text={name}').wait_for(timeout=5000)

    async def is_label_visible_in_modal(self, name: str) -> bool:
        """Check whether a label is visible inside the labels modal."""
        try:
            await self.page.locator(self.labels_modal).locator(f'text={name}').wait_for(timeout=3000)
            return True
        except:
            return False

    async def open_filters(self):
        """Open the filters sidebar."""
        logger.info("Opening filters sidebar")
        await self.page.click(self.filters_button)
        await self.page.wait_for_selector(self.filter_sidebar, timeout=5000)

    async def filter_by_title(self, title: str):
        """Apply a title filter from the sidebar."""
        logger.info(f"Filtering by title: {title}")
        async with self.page.expect_response(_is_notes_response):
            await self.page.fill(self.title_filter_input, title)
            await self.page.wait_for_timeout(450)
        await self.wait_until_loaded()

    async def toggle_label_filter(self, label_name: str):
        """Toggle a label filter by label name."""
        logger.info(f"Toggling label filter: {label_name}")
        async with self.page.expect_response(_is_notes_response):
            await self.page.locator(self.filter_sidebar).locator('label', has_text=label_name).click()
        await self.wait_until_loaded()

    async def clear_filters(self):
        """Clear all active filters."""
        logger.info("Clearing filters")
        async with self.page.expect_response(_is_notes_response):
            await self.page.click(self.clear_filters_button)
        await self.wait_until_loaded()

    async def is_no_filter_results_visible(self) -> bool:
        """Check whether the no-results filtered state is visible."""
        try:
            await self.page.wait_for_selector(self.no_filter_results, timeout=3000)
            return True
        except:
            return False
    
    async def click_logout(self):
        """Click logout button."""
        logger.info("Clicking logout button")
        await self.page.click(self.logout_button)
        await self.page.wait_for_url(f"{self.base_url}/login", timeout=5000)
    
    async def is_logged_in(self) -> bool:
        """Check if logout button is visible (indicates logged in)."""
        try:
            await self.page.wait_for_selector(self.logout_button, timeout=2000)
            return True
        except:
            return False
