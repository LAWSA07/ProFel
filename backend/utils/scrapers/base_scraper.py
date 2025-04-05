from abc import ABC, abstractmethod
from typing import Dict, Any, List
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import logging
import datetime

class BaseScraper(ABC):
    def __init__(self):
        self.session = None
        self.browser = None
        self.logger = logging.getLogger(__name__)

    async def init_session(self):
        """Initialize aiohttp session for basic requests"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def init_browser(self):
        """Initialize playwright browser for JavaScript-heavy pages"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)

    @abstractmethod
    async def extract_profile_data(self, profile_url: str) -> Dict[str, Any]:
        """Extract profile data from the given URL"""
        pass

    @abstractmethod
    async def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills from the profile page"""
        pass

    @abstractmethod
    async def extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract projects from the profile page"""
        pass

    async def get_page_content(self, url: str) -> str:
        """Get page content using playwright for better JavaScript handling"""
        try:
            await self.init_browser()
            page = await self.browser.new_page()
            await page.goto(url, wait_until="networkidle")
            content = await page.content()
            await page.close()
            return content
        except Exception as e:
            self.logger.error(f"Error fetching page with playwright: {e}")
            # Fallback to simple HTTP request if browser fails
            await self.init_session()
            async with self.session.get(url) as response:
                return await response.text()

    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        if self.browser:
            await self.browser.close()

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        return ' '.join(text.split())

    async def retry_with_backoff(self, func, *args, max_retries=3, initial_delay=1):
        """Retry function with exponential backoff"""
        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return await func(*args)
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2

        raise last_exception