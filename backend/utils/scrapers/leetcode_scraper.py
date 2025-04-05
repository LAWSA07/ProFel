from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from .base_scraper import BaseScraper

class LeetCodeScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"

    async def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """Extract LeetCode profile data"""
        profile_url = f"https://leetcode.com/{username}/"
        content = await self.retry_with_backoff(
            self.get_page_content, profile_url
        )

        soup = BeautifulSoup(content, 'html.parser')

        # Extract profile data using GraphQL
        profile_query = {
            "query": """
            query userPublicProfile($username: String!) {
                matchedUser(username: $username) {
                    username
                    profile {
                        realName
                        websites
                        countryName
                        skillTags
                        company
                        school
                        starRating
                        aboutMe
                        userAvatar
                        reputation
                        ranking
                    }
                    submitStats {
                        acSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    }
                }
            }
            """,
            "variables": {"username": username}
        }

        # Get profile data
        profile_data = await self._fetch_graphql_data(profile_query)
        user_data = profile_data.get('data', {}).get('matchedUser', {})

        # Get solved problems data
        problems_data = await self._fetch_solved_problems(username)

        return {
            'username': username,
            'profile': user_data.get('profile', {}),
            'stats': user_data.get('submitStats', {}),
            'solved_problems': problems_data,
            'skills': await self.extract_skills(soup),
            'recent_submissions': await self._fetch_recent_submissions(username)
        }

    async def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills from LeetCode profile"""
        skills = set()

        # Extract from problem solutions
        script_tags = soup.select('script[type="application/json"]')
        for script in script_tags:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and 'userLanguages' in data:
                    skills.update(data['userLanguages'])
            except (json.JSONDecodeError, AttributeError):
                continue

        return list(skills)

    async def extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract projects from LeetCode profile (not applicable)"""
        return []

    async def _fetch_graphql_data(self, query: Dict) -> Dict:
        """Fetch data using LeetCode's GraphQL API"""
        async with self.session.post(self.graphql_url, json=query) as response:
            return await response.json()

    async def _fetch_solved_problems(self, username: str) -> List[Dict[str, Any]]:
        """Fetch solved problems data"""
        query = {
            "query": """
            query userProblemsSolved($username: String!) {
                allQuestionsCount {
                    difficulty
                    count
                }
                matchedUser(username: $username) {
                    problemsSolvedBeatsStats {
                        difficulty
                        percentage
                    }
                    submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """,
            "variables": {"username": username}
        }

        data = await self._fetch_graphql_data(query)
        return data.get('data', {})

    async def _fetch_recent_submissions(self, username: str) -> List[Dict[str, Any]]:
        """Fetch recent submissions"""
        query = {
            "query": """
            query recentSubmissions($username: String!) {
                recentSubmissionList(username: $username) {
                    title
                    timestamp
                    statusDisplay
                    lang
                }
            }
            """,
            "variables": {"username": username}
        }

        data = await self._fetch_graphql_data(query)
        return data.get('data', {}).get('recentSubmissionList', [])