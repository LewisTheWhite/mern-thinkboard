"""
Login page object model.
"""

import logging

logger = logging.getLogger(__name__)


class LoginPage:
    """Page object for login page."""
    
    def __init__(self, page):
        """Initialize login page."""
        self.page = page
        self.base_url = "http://localhost:5173"
        
        # Selectors
        self.email_input = '#login-email'
        self.password_input = '#login-password'
        self.login_button = 'button:has-text("Sign In")'
        self.error_message = '.text-error, [role="alert"], [role="status"]'
    
    async def navigate(self):
        """Navigate to login page."""
        logger.info("Navigating to login page")
        await self.page.goto(f"{self.base_url}/login")
        await self.page.wait_for_url(f"{self.base_url}/login")
        await self.page.wait_for_selector(self.email_input, timeout=5000)
    
    async def fill_email(self, email: str):
        """Enter email address."""
        logger.info(f"Entering email: {email}")
        await self.page.fill(self.email_input, email)
    
    async def fill_password(self, password: str):
        """Enter password."""
        logger.info("Entering password")
        await self.page.fill(self.password_input, password)
    
    async def click_login(self):
        """Click login button."""
        logger.info("Clicking login button")
        await self.page.click(self.login_button)
    
    async def login(self, email: str, password: str):
        """Complete login flow."""
        await self.fill_email(email)
        await self.fill_password(password)
        await self.click_login()
        # Wait for navigation or error
        await self.page.wait_for_url(f"{self.base_url}/", timeout=5000)
    
    async def get_error_message(self) -> str:
        """Get error message if login failed."""
        try:
            await self.page.wait_for_selector('text=Invalid credentials', timeout=5000)
            return 'Invalid credentials'
        except:
            try:
                await self.page.wait_for_selector(self.error_message, timeout=2000)
                return await self.page.text_content(self.error_message)
            except:
                return None
    
    async def is_logged_in(self) -> bool:
        """Check if successfully logged in."""
        current_url = self.page.url
        return current_url == f"{self.base_url}/"
