import logging
import asyncio
from typing import Dict, Any, List, Union

from .scrapers.scraper_factory import ScraperFactory
from .profile_manager import ProfileManager
from .matching_engine import MatchingEngine

class APIWrapper:
    """
    Wrapper for API endpoints to coordinate different components
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.profile_manager = ProfileManager()
        self.matching_engine = MatchingEngine()

    async def fetch_profile(self, platform: str, username: str, session_id: str = None) -> Dict[str, Any]:
        """
        Fetch a profile from a platform

        Args:
            platform: Platform name (github, leetcode, etc.)
            username: Username or handle on the platform
            session_id: Optional session ID for tracking

        Returns:
            Processed profile data
        """
        try:
            # Get the appropriate scraper
            scraper = ScraperFactory.get_scraper(platform)

            # Fetch profile data
            profile_data = await scraper.extract_profile_data(username)

            # Clean up resources
            await scraper.cleanup()

            # Process profile for matching
            processed_profile = self.matching_engine.process_profile(profile_data, platform)

            return {
                "status": "success",
                "profile": processed_profile
            }

        except Exception as e:
            self.logger.error(f"Error fetching profile: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch profile: {str(e)}"
            }

    async def fetch_multi_platform_profile(self, platform_usernames: Dict[str, str],
                                         session_id: str = None) -> Dict[str, Any]:
        """
        Fetch profiles from multiple platforms

        Args:
            platform_usernames: Dictionary mapping platform names to usernames
                              e.g., {'github': 'user1', 'leetcode': 'user2'}
            session_id: Optional session ID for tracking

        Returns:
            Combined profile data from all platforms
        """
        try:
            # Use the profile manager to fetch data from multiple platforms
            aggregated_data = await self.profile_manager.get_profile_data(platform_usernames)

            return {
                "status": "success",
                "profile": aggregated_data
            }

        except Exception as e:
            self.logger.error(f"Error fetching multi-platform profile: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch multi-platform profile: {str(e)}",
                "platforms_fetched": []
            }

    def create_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job listing

        Args:
            job_data: Job details including title, company, description, skills

        Returns:
            Processed job data with ID
        """
        try:
            # Process job for matching
            processed_job = self.matching_engine.process_job(job_data)

            return {
                "status": "success",
                "job": processed_job
            }

        except Exception as e:
            self.logger.error(f"Error creating job: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create job: {str(e)}"
            }

    def match_profile_to_jobs(self, platform: str, username: str,
                            job_ids: List[int] = None) -> Dict[str, Any]:
        """
        Match a profile against jobs

        Args:
            platform: Platform name (github, leetcode, etc.)
            username: Username or handle on the platform
            job_ids: Optional list of job IDs to match against (otherwise all jobs)

        Returns:
            Matching results with scores
        """
        try:
            # Use matching engine to find matches
            matches = self.matching_engine.match_profile_to_jobs(
                username=username,
                platform=platform,
                job_ids=job_ids
            )

            return {
                "status": "success",
                "matches": matches,
                "match_count": len(matches)
            }

        except Exception as e:
            self.logger.error(f"Error matching profile to jobs: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to match profile to jobs: {str(e)}"
            }

    def calculate_match_score(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate match score between a profile and a job

        Args:
            profile: Profile data
            job: Job data

        Returns:
            Match score data
        """
        try:
            return self.matching_engine.calculate_match_score(profile, job)
        except Exception as e:
            self.logger.error(f"Error calculating match score: {str(e)}")
            # Return a fallback score with error info
            return {
                "overall_score": 0.5,
                "error": str(e)
            }

    def combine_profiles(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine multiple profiles from different platforms

        Args:
            profiles: List of profiles from different platforms

        Returns:
            Combined profile data
        """
        try:
            return self.matching_engine.combine_profiles(profiles)
        except Exception as e:
            self.logger.error(f"Error combining profiles: {str(e)}")
            return {
                "error": str(e),
                "profiles_count": len(profiles)
            }

    def calculate_combined_match(self, profiles: List[Dict[str, Any]], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate match using combined data from multiple profiles

        Args:
            profiles: List of profiles from different platforms
            job: Job data

        Returns:
            Match result with score and details
        """
        try:
            return self.matching_engine.match_combined_profile_to_job(profiles, job)
        except Exception as e:
            self.logger.error(f"Error calculating combined match: {str(e)}")
            # Return a fallback score with error info
            return {
                "overall_score": 0.5,
                "error": str(e),
                "platforms": [p.get("platform", "unknown") for p in profiles]
            }

    def get_supported_platforms(self) -> Dict[str, Any]:
        """Get list of supported platforms"""
        try:
            platforms = self.profile_manager.get_supported_platforms()

            return {
                "status": "success",
                "platforms": platforms
            }

        except Exception as e:
            self.logger.error(f"Error getting supported platforms: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get supported platforms: {str(e)}"
            }

    async def validate_profile(self, platform: str, username: str) -> Dict[str, Any]:
        """
        Validate if a profile exists and is accessible

        Args:
            platform: Platform name
            username: Username to validate

        Returns:
            Validation result
        """
        try:
            is_valid = await self.profile_manager.validate_profile(platform, username)

            if is_valid:
                return {
                    "status": "success",
                    "valid": True,
                    "message": f"Profile {username} found on {platform}"
                }
            else:
                return {
                    "status": "success",
                    "valid": False,
                    "message": f"Profile {username} not found on {platform}"
                }

        except Exception as e:
            self.logger.error(f"Error validating profile: {str(e)}")
            return {
                "status": "error",
                "valid": False,
                "message": f"Failed to validate profile: {str(e)}"
            }