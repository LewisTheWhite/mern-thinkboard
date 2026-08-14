"""
Note detail page object model.
"""

import logging

logger = logging.getLogger(__name__)


class NotePage:
    """Page object for individual note detail page."""
    
    def __init__(self, page):
        """Initialize note page."""
        self.page = page
        self.base_url = "http://localhost:5173"
        
        # Selectors
        self.note_title = 'h1, h2'  # Adjust based on actual structure
        self.note_content = 'p, .content'  # Adjust based on actual structure
        self.edit_button = 'button:has-text("Edit")'
        self.delete_button = 'button:has-text("Delete")'
        self.back_button = 'button:has-text("Back")'
        self.save_button = 'button:has-text("Save")'
        self.title_input = 'input[name="title"]'
        self.content_input = 'textarea'
        self.success_toast = 'div.toast'
    
    async def navigate_to_note(self, note_id: str):
        """Navigate to specific note by ID."""
        logger.info(f"Navigating to note: {note_id}")
        await self.page.goto(f"{self.base_url}/note/{note_id}")
        await self.page.wait_for_selector(self.note_title, timeout=5000)
    
    async def get_title(self) -> str:
        """Get note title."""
        return await self.page.text_content(self.note_title)
    
    async def get_content(self) -> str:
        """Get note content."""
        return await self.page.text_content(self.note_content)
    
    async def click_edit(self):
        """Click edit button to enter edit mode."""
        logger.info("Clicking edit button")
        await self.page.click(self.edit_button)
        await self.page.wait_for_selector(self.title_input, timeout=2000)
    
    async def update_title(self, new_title: str):
        """Update note title."""
        logger.info(f"Updating title to: {new_title}")
        await self.page.fill(self.title_input, new_title)
    
    async def update_content(self, new_content: str):
        """Update note content."""
        logger.info("Updating content")
        await self.page.fill(self.content_input, new_content)
    
    async def click_save(self):
        """Click save button."""
        logger.info("Clicking save button")
        await self.page.click(self.save_button)
        await self.page.wait_for_selector(self.success_toast, timeout=3000)
    
    async def click_delete(self):
        """Click delete button."""
        logger.info("Clicking delete button")
        await self.page.click(self.delete_button)
        # Handle potential confirmation dialog
        try:
            await self.page.click('button:has-text("Confirm")', timeout=2000)
        except:
            pass
        # Wait for redirect to home
        await self.page.wait_for_url(f"{self.base_url}/", timeout=5000)
    
    async def click_back(self):
        """Click back button to return to notes list."""
        logger.info("Clicking back button")
        await self.page.click(self.back_button)
        await self.page.wait_for_url(f"{self.base_url}/", timeout=5000)
