from typing import Dict, Any, List
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper

class GitHubScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://github.com"

    async def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """Extract GitHub profile data"""
        profile_url = f"{self.base_url}/{username}"
        content = await self.retry_with_backoff(
            self.get_page_content, profile_url
        )

        soup = BeautifulSoup(content, 'html.parser')

        # Extract basic profile information
        profile_data = {
            'username': username,
            'name': self._extract_name(soup),
            'bio': self._extract_bio(soup),
            'location': self._extract_location(soup),
            'email': self._extract_email(soup),
            'website': self._extract_website(soup),
            'company': self._extract_company(soup),
            'followers': self._extract_followers(soup),
            'following': self._extract_following(soup),
            'contributions': await self._extract_contributions(username),
            'skills': await self.extract_skills(soup),
            'projects': await self.extract_projects(soup),
            'repositories': await self._extract_repositories(username)
        }

        return profile_data

    async def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills from GitHub profile"""
        skills = set()

        # Extract from pinned repositories
        for repo in soup.select('[itemprop="owns"] .pinned-item-list-item'):
            # Extract languages used
            for lang in repo.select('.repo-language-color + span'):
                skills.add(lang.text.strip())

            # Extract from repository description
            desc = repo.select_one('.pinned-item-desc')
            if desc:
                # Use common programming terms regex
                tech_terms = re.findall(r'\b(?:Python|JavaScript|React|Node\.js|SQL|Java|C\+\+|Ruby|Go|Rust|PHP|HTML|CSS|TypeScript|Angular|Vue\.js|Django|Flask|Spring|Express\.js|MongoDB|PostgreSQL|MySQL|Redis|Docker|Kubernetes|AWS|Azure|GCP|Git|CI/CD|REST|GraphQL|API|ML|AI|DevOps)\b', desc.text)
                skills.update(tech_terms)

        return list(skills)

    async def extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract projects from GitHub profile"""
        projects = []

        # Extract from pinned repositories
        for repo in soup.select('[itemprop="owns"] .pinned-item-list-item'):
            project = {
                'name': self._clean_text(repo.select_one('a[itemprop="name codeRepository"]').text),
                'description': '',
                'language': '',
                'stars': '0',
                'forks': '0'
            }

            # Get description
            desc_elem = repo.select_one('.pinned-item-desc')
            if desc_elem:
                project['description'] = self._clean_text(desc_elem.text)

            # Get primary language
            lang_elem = repo.select_one('.repo-language-color + span')
            if lang_elem:
                project['language'] = self._clean_text(lang_elem.text)

            # Get stars and forks
            stats = repo.select('.pinned-item-meta')
            if len(stats) >= 2:
                project['stars'] = self._clean_text(stats[0].text)
                project['forks'] = self._clean_text(stats[1].text)

            projects.append(project)

        return projects

    async def _extract_repositories(self, username: str) -> List[Dict[str, str]]:
        """Extract repository information"""
        repos_url = f"{self.base_url}/{username}?tab=repositories"
        content = await self.retry_with_backoff(
            self.get_page_content, repos_url
        )

        soup = BeautifulSoup(content, 'html.parser')
        repos = []

        for repo in soup.select('#user-repositories-list li'):
            repo_data = {
                'name': '',
                'description': '',
                'language': '',
                'stars': '0',
                'forks': '0',
                'updated': ''
            }

            name_elem = repo.select_one('h3 a')
            if name_elem:
                repo_data['name'] = self._clean_text(name_elem.text)

            desc_elem = repo.select_one('p')
            if desc_elem:
                repo_data['description'] = self._clean_text(desc_elem.text)

            lang_elem = repo.select_one('[itemprop="programmingLanguage"]')
            if lang_elem:
                repo_data['language'] = self._clean_text(lang_elem.text)

            # Extract stars and forks
            stats = repo.select('a.Link--muted')
            if len(stats) >= 2:
                repo_data['stars'] = self._clean_text(stats[0].text)
                repo_data['forks'] = self._clean_text(stats[1].text)

            updated_elem = repo.select_one('relative-time')
            if updated_elem:
                repo_data['updated'] = updated_elem.get('datetime', '')

            repos.append(repo_data)

        return repos

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract user's full name"""
        name_elem = soup.select_one('h1.vcard-names span.p-name')
        return self._clean_text(name_elem.text) if name_elem else ''

    def _extract_bio(self, soup: BeautifulSoup) -> str:
        """Extract user's bio"""
        bio_elem = soup.select_one('.user-profile-bio')
        return self._clean_text(bio_elem.text) if bio_elem else ''

    def _extract_location(self, soup: BeautifulSoup) -> str:
        """Extract user's location"""
        location_elem = soup.select_one('[itemprop="homeLocation"]')
        return self._clean_text(location_elem.text) if location_elem else ''

    def _extract_email(self, soup: BeautifulSoup) -> str:
        """Extract user's email"""
        email_elem = soup.select_one('[itemprop="email"]')
        return self._clean_text(email_elem.text) if email_elem else ''

    def _extract_website(self, soup: BeautifulSoup) -> str:
        """Extract user's website"""
        website_elem = soup.select_one('[itemprop="url"]')
        return website_elem.get('href', '') if website_elem else ''

    def _extract_company(self, soup: BeautifulSoup) -> str:
        """Extract user's company"""
        company_elem = soup.select_one('[itemprop="worksFor"]')
        return self._clean_text(company_elem.text) if company_elem else ''

    def _extract_followers(self, soup: BeautifulSoup) -> str:
        """Extract number of followers"""
        followers_elem = soup.select_one('.js-profile-editable-area a[href$="?tab=followers"] .text-bold')
        return self._clean_text(followers_elem.text) if followers_elem else '0'

    def _extract_following(self, soup: BeautifulSoup) -> str:
        """Extract number of users being followed"""
        following_elem = soup.select_one('.js-profile-editable-area a[href$="?tab=following"] .text-bold')
        return self._clean_text(following_elem.text) if following_elem else '0'

    async def _extract_contributions(self, username: str) -> Dict[str, Any]:
        """Extract contribution information"""
        contributions_url = f"{self.base_url}/{username}"
        content = await self.retry_with_backoff(
            self.get_page_content, contributions_url
        )

        soup = BeautifulSoup(content, 'html.parser')

        # Get total contributions
        total_elem = soup.select_one('.js-yearly-contributions h2')
        total = '0'
        if total_elem:
            match = re.search(r'\d+', total_elem.text)
            if match:
                total = match.group()

        return {
            'total': total,
            'streak': self._extract_streak(soup)
        }

    def _extract_streak(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contribution streak information"""
        streak_elem = soup.select_one('.js-yearly-contributions .f4')
        streak = {'current': '0', 'longest': '0'}

        if streak_elem:
            streak_text = streak_elem.text
            current_match = re.search(r'Current streak: (\d+)', streak_text)
            longest_match = re.search(r'Longest streak: (\d+)', streak_text)

            if current_match:
                streak['current'] = current_match.group(1)
            if longest_match:
                streak['longest'] = longest_match.group(1)

        return streak