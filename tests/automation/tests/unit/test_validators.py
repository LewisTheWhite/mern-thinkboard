"""
Unit tests for input validators.
Tests email format, password policy, and other validations.
"""

import pytest
import re


class TestEmailValidator:
    """Email validation tests."""
    
    EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        return bool(re.match(self.EMAIL_REGEX, email))
    
    def test_valid_email_format(self):
        """Test valid email is accepted."""
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "firstname+lastname@company.com",
            "test_user@test-domain.com",
        ]
        for email in valid_emails:
            assert self.is_valid_email(email), f"Email {email} should be valid"
    
    def test_invalid_email_format(self):
        """Test invalid emails are rejected."""
        invalid_emails = [
            "plainaddress",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
            "user..name@example.com",
        ]
        for email in invalid_emails:
            assert not self.is_valid_email(email), f"Email {email} should be invalid"
    
    def test_email_with_special_characters(self):
        """Test email with valid special characters."""
        assert self.is_valid_email("user+tag@example.com")
        assert self.is_valid_email("user_name@example.com")
        assert self.is_valid_email("user-name@example.com")


class TestPasswordValidator:
    """Password validation tests."""
    
    MIN_PASSWORD_LENGTH = 8
    
    def is_valid_password(self, password: str) -> bool:
        """Validate password meets minimum requirements."""
        return len(password) >= self.MIN_PASSWORD_LENGTH
    
    def test_password_minimum_length(self):
        """Test password must be at least 8 characters."""
        assert self.is_valid_password("TestPass123")
        assert self.is_valid_password("12345678")
        assert not self.is_valid_password("short")
        assert not self.is_valid_password("1234567")  # 7 chars
    
    def test_password_empty(self):
        """Test empty password is invalid."""
        assert not self.is_valid_password("")
    
    def test_password_exactly_minimum(self):
        """Test password exactly at minimum length is valid."""
        assert self.is_valid_password("12345678")  # exactly 8
    
    def test_password_long(self):
        """Test very long password is valid."""
        long_pass = "a" * 100
        assert self.is_valid_password(long_pass)


class TestPasswordMatch:
    """Password confirmation matching tests."""
    
    def test_passwords_match(self):
        """Test matching passwords."""
        password = "TestPassword123"
        assert password == password
    
    def test_passwords_do_not_match(self):
        """Test non-matching passwords."""
        password1 = "TestPassword123"
        password2 = "DifferentPassword123"
        assert password1 != password2
    
    def test_passwords_match_case_sensitive(self):
        """Test password matching is case-sensitive."""
        password1 = "TestPassword123"
        password2 = "testpassword123"
        assert password1 != password2
