"""
User factory for generating test user data.
"""

from datetime import datetime
from typing import Dict

from faker import Faker

from settings import config

fake = Faker()


class UserFactory:
    """Factory for creating test user objects."""
    
    @staticmethod
    def create(
        name: str = None,
        email: str = None,
        password: str = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Create a test user object.
        
        Args:
            name: User full name (default: Test User)
            email: User email (default: unique generated email)
            password: User password (default: configured test password)
            **kwargs: Additional fields to include
            
        Returns:
            Dictionary with user data
        """
        if email is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[-6:]
            email = f"testuser_{timestamp}_{fake.random_int(1000, 9999)}@test.com"
        
        user_data = {
            "name": name or config.test_data.TEST_USER_NAME,
            "email": email,
            "password": password or config.test_data.TEST_PASSWORD,
            "confirmPassword": password or config.test_data.TEST_PASSWORD,
        }
        
        user_data.update(kwargs)
        return user_data
    
    @staticmethod
    def create_invalid_email() -> Dict[str, str]:
        """Create user with invalid email."""
        return UserFactory.create(email="invalidemail")
    
    @staticmethod
    def create_invalid_password() -> Dict[str, str]:
        """Create user with invalid (short) password."""
        return UserFactory.create(password="short")
    
    @staticmethod
    def create_password_mismatch() -> Dict[str, str]:
        """Create user with mismatched password confirmation."""
        user = UserFactory.create()
        user["confirmPassword"] = "DifferentPassword123!"
        return user
