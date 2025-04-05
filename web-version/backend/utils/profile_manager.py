from typing import Dict, Any, List
import asyncio
from .scrapers.scraper_factory import ScraperFactory
import logging

class ProfileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scraper_factory = ScraperFactory

    async def get_profile_data(self, platform_usernames: Dict[str, str]) -> Dict[str, Any]:
        """
        Fetch profile data from multiple platforms

        Args:
            platform_usernames: Dictionary mapping platform names to usernames
                              e.g., {'github': 'user1', 'leetcode': 'user2'}
        """
        tasks = []
        for platform, username in platform_usernames.items():
            if not username:
                continue

            try:
                scraper = self.scraper_factory.get_scraper(platform)
                tasks.append(self._fetch_platform_data(scraper, username))
            except ValueError as e:
                self.logger.warning(f"Skipping unsupported platform: {platform}")
                continue

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle any exceptions
        processed_data = {}
        for platform, result in zip(platform_usernames.keys(), results):
            if isinstance(result, Exception):
                self.logger.error(f"Error fetching data from {platform}: {str(result)}")
                continue
            processed_data[platform] = result

        return self._aggregate_profile_data(processed_data)

    async def _fetch_platform_data(self, scraper, username: str) -> Dict[str, Any]:
        """Fetch data from a single platform"""
        try:
            data = await scraper.extract_profile_data(username)
            await scraper.cleanup()
            return data
        except Exception as e:
            self.logger.error(f"Error in _fetch_platform_data: {str(e)}")
            raise

    def _aggregate_profile_data(self, platform_data: Dict[str, Dict]) -> Dict[str, Any]:
        """Aggregate data from multiple platforms into a unified profile"""
        aggregated = {
            'skills': set(),
            'projects': [],
            'contributions': {},
            'platforms': {}
        }

        for platform, data in platform_data.items():
            # Add platform-specific data
            aggregated['platforms'][platform] = data

            # Aggregate skills
            if 'skills' in data:
                aggregated['skills'].update(data['skills'])

            # Aggregate projects (mainly from GitHub)
            if platform == 'github' and 'projects' in data:
                aggregated['projects'].extend(data['projects'])

            # Aggregate contributions
            if 'contributions' in data:
                aggregated['contributions'][platform] = data['contributions']

        # Convert skills set to sorted list
        aggregated['skills'] = sorted(list(aggregated['skills']))

        return aggregated

    def get_supported_platforms(self) -> List[str]:
        """Get list of supported platforms"""
        return self.scraper_factory.get_supported_platforms()

    async def validate_profile(self, platform: str, username: str) -> bool:
        """Validate if a profile exists and is accessible"""
        try:
            scraper = self.scraper_factory.get_scraper(platform)
            await scraper.extract_profile_data(username)
            await scraper.cleanup()
            return True
        except Exception as e:
            self.logger.error(f"Profile validation failed: {str(e)}")
            return False