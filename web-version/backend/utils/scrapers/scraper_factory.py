from typing import Dict, Type
from .base_scraper import BaseScraper
from .github_scraper import GitHubScraper
from .leetcode_scraper import LeetCodeScraper
from .codeforces_scraper import CodeforcesScraper
from .linkedin_scraper import LinkedInScraper

class ScraperFactory:
    _scrapers: Dict[str, Type[BaseScraper]] = {
        'github': GitHubScraper,
        'leetcode': LeetCodeScraper,
        'codeforces': CodeforcesScraper,
        'linkedin': LinkedInScraper
    }

    @classmethod
    def get_scraper(cls, platform: str) -> BaseScraper:
        """Get a scraper instance for the specified platform"""
        scraper_class = cls._scrapers.get(platform.lower())
        if not scraper_class:
            raise ValueError(f"No scraper available for platform: {platform}")
        return scraper_class()

    @classmethod
    def get_supported_platforms(cls) -> list:
        """Get list of supported platforms"""
        return list(cls._scrapers.keys())

    @classmethod
    def register_scraper(cls, platform: str, scraper_class: Type[BaseScraper]):
        """Register a new scraper for a platform"""
        cls._scrapers[platform.lower()] = scraper_class