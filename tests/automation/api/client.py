"""
HTTP API client for making requests to the backend.
Handles authentication, retries, and response validation.
"""

import logging
from typing import Any, Dict, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from settings import config

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client for API testing with auth support."""
    
    def __init__(self, base_url: str = config.api.BASE_URL, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            base_url=base_url,
            timeout=config.api.TIMEOUT,
        )
    
    def set_token(self, token: str):
        """Set authentication token."""
        self.token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token if available."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    @retry(stop=stop_after_attempt(config.api.RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make GET request."""
        logger.info(f"GET {self.base_url}/{endpoint}")
        response = self.client.get(endpoint, headers=self._get_headers(), **kwargs)
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    @retry(stop=stop_after_attempt(config.api.RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> httpx.Response:
        """Make POST request."""
        logger.info(f"POST {self.base_url}/{endpoint}")
        logger.debug(f"Payload: {json}")
        response = self.client.post(endpoint, headers=self._get_headers(), json=json, **kwargs)
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    @retry(stop=stop_after_attempt(config.api.RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> httpx.Response:
        """Make PUT request."""
        logger.info(f"PUT {self.base_url}/{endpoint}")
        logger.debug(f"Payload: {json}")
        response = self.client.put(endpoint, headers=self._get_headers(), json=json, **kwargs)
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    @retry(stop=stop_after_attempt(config.api.RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make DELETE request."""
        logger.info(f"DELETE {self.base_url}/{endpoint}")
        response = self.client.delete(endpoint, headers=self._get_headers(), **kwargs)
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    def close(self):
        """Close HTTP client."""
        self.client.close()
