"""
Signup page object model.
"""

import logging

logger = logging.getLogger(__name__)


class SignupPage:
    """Page object for signup page."""
    
    def __init__(self, page):
        """Initialize signup page."""
        self.page = page
        self.base_url = "http://localhost:5173"
        
        # Selectors
        self.name_input = '#signup-name'
        self.email_input = '#signup-email'
        self.password_input = '#signup-password'
        self.confirm_password_input = '#signup-confirm-password'
        self.signup_button = 'button:has-text("Create Account")'
        self.error_message = '.text-error, [role="alert"], [role="status"]'
    
    async def navigate(self):
        """Navigate to signup page."""
        logger.info("Navigating to signup page")
        await self.page.goto(f"{self.base_url}/signup")
        await self.page.wait_for_url(f"{self.base_url}/signup")
        await self.page.wait_for_selector(self.name_input, timeout=5000)
    
    async def fill_name(self, name: str):
        """Enter name."""
        logger.info(f"Entering name: {name}")
        await self.page.fill(self.name_input, name)
    
    async def fill_email(self, email: str):
        """Enter email address."""
        logger.info(f"Entering email: {email}")
        await self.page.fill(self.email_input, email)
    
    async def fill_password(self, password: str):
        """Enter password."""
        logger.info("Entering password")
        await self.page.fill(self.password_input, password)
    
    async def fill_confirm_password(self, password: str):
        """Enter password confirmation."""
        logger.info("Entering password confirmation")
        await self.page.fill(self.confirm_password_input, password)
    
    async def click_signup(self):
        """Click signup button."""
        logger.info("Clicking signup button")
        await self.page.click(self.signup_button)
    
    async def signup(self, name: str, email: str, password: str):
        """Complete signup flow."""
        await self.fill_name(name)
        await self.fill_email(email)
        await self.fill_password(password)
        await self.fill_confirm_password(password)
        await self.click_signup()
        # Wait for toast or navigation to login
        await self.page.wait_for_url(f"{self.base_url}/login", timeout=5000)
    
    async def get_error_message(self) -> str:
        """Get error message if signup failed."""
        try:
            await self.page.wait_for_selector(self.error_message, timeout=2000)
            return await self.page.text_content(self.error_message)
        except:
            return None
    
    async def is_signup_success(self) -> bool:
        """Check if successfully signed up (redirected to login)."""
        current_url = self.page.url
        return current_url == f"{self.base_url}/login"
