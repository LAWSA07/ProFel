from typing import Dict, Any, List
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper

class CodeforcesScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://codeforces.com"
        self.api_url = "https://codeforces.com/api"

    async def extract_profile_data(self, handle: str) -> Dict[str, Any]:
        """Extract Codeforces profile data"""
        profile_url = f"https://codeforces.com/profile/{handle}"
        content = await self.retry_with_backoff(
            self.get_page_content, profile_url
        )

        soup = BeautifulSoup(content, 'html.parser')

        # Get user info from API
        user_info = await self._fetch_user_info(handle)

        # Get submissions from API
        submissions = await self._fetch_user_submissions(handle)

        # Get contests from API
        contests = await self._fetch_user_contests(handle)

        profile_data = {
            'handle': handle,
            'info': user_info,
            'rating': self._extract_rating(soup),
            'rank': self._extract_rank(soup),
            'max_rating': self._extract_max_rating(soup),
            'contributions': self._extract_contributions(soup),
            'skills': await self.extract_skills(soup),
            'submissions': submissions,
            'contests': contests
        }

        return profile_data

    async def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills from Codeforces profile"""
        skills = set()

        # Extract from solved problems
        for submission in soup.select('.personal-sidebar'):
            # Extract programming languages used
            langs = submission.select('.smaller')
            for lang in langs:
                if 'C++' in lang.text or 'Python' in lang.text or 'Java' in lang.text:
                    skills.add(lang.text.strip())

        # Extract from problem tags
        for tag in soup.select('.tag-box'):
            skills.add(tag.text.strip())

        return list(skills)

    async def extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract projects from Codeforces profile (not applicable)"""
        return []

    async def _fetch_user_info(self, handle: str) -> Dict[str, Any]:
        """Fetch user info from Codeforces API"""
        url = f"{self.api_url}/user.info?handles={handle}"
        async with self.session.get(url) as response:
            data = await response.json()
            if data['status'] == 'OK':
                return data['result'][0]
            return {}

    async def _fetch_user_submissions(self, handle: str) -> List[Dict[str, Any]]:
        """Fetch user submissions from Codeforces API"""
        url = f"{self.api_url}/user.status?handle={handle}&from=1&count=100"
        async with self.session.get(url) as response:
            data = await response.json()
            if data['status'] == 'OK':
                return data['result']
            return []

    async def _fetch_user_contests(self, handle: str) -> List[Dict[str, Any]]:
        """Fetch user contest history from Codeforces API"""
        url = f"{self.api_url}/user.rating?handle={handle}"
        async with self.session.get(url) as response:
            data = await response.json()
            if data['status'] == 'OK':
                return data['result']
            return []

    def _extract_rating(self, soup: BeautifulSoup) -> str:
        """Extract current rating"""
        rating_elem = soup.select_one('.info ul li span')
        if rating_elem:
            match = re.search(r'\d+', rating_elem.text)
            if match:
                return match.group()
        return '0'

    def _extract_rank(self, soup: BeautifulSoup) -> str:
        """Extract current rank"""
        rank_elem = soup.select_one('.user-rank span')
        return rank_elem.text.strip() if rank_elem else ''

    def _extract_max_rating(self, soup: BeautifulSoup) -> str:
        """Extract maximum rating achieved"""
        max_rating_elem = soup.select_one('.info ul li span[style*="color:"]')
        if max_rating_elem:
            match = re.search(r'\d+', max_rating_elem.text)
            if match:
                return match.group()
        return '0'

    def _extract_contributions(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contribution information"""
        contributions = {
            'problems_solved': '0',
            'contests_participated': '0'
        }

        # Extract problems solved
        solved_elem = soup.select_one('.info ul li:contains("solved")')
        if solved_elem:
            match = re.search(r'\d+', solved_elem.text)
            if match:
                contributions['problems_solved'] = match.group()

        # Extract contest count
        contests_elem = soup.select_one('.info ul li:contains("Contest")')
        if contests_elem:
            match = re.search(r'\d+', contests_elem.text)
            if match:
                contributions['contests_participated'] = match.group()

        return contributions