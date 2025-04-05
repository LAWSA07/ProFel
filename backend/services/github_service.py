import os
import asyncio
from typing import Dict, List, Optional
from dotenv import load_dotenv
import time

# Import original GitHub scraping code (modified for web API)
from utils.github_utils import get_browser_config, scrape_github_profile

# Load environment variables
load_dotenv()

async def process_github_profile(username: str) -> Dict:
    """
    Process a GitHub profile and extract relevant information.

    Args:
        username: GitHub username

    Returns:
        Dict: Extracted profile data
    """
    from crawl4ai import AsyncWebCrawler

    # Initialize browser configuration
    browser_config = get_browser_config()
    session_id = f"profile_{username}_{int(time.time())}"

    # Initialize profile data
    profile_data = {}

    try:
        # Start the web crawler
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # Scrape GitHub profile
            github_data = await scrape_github_profile(crawler, username, session_id)

            # In the future, add LinkedIn and LeetCode scrapers
            # linkedin_data = await scrape_linkedin_profile(crawler, linkedin_username, session_id)
            # leetcode_data = await scrape_leetcode_profile(crawler, leetcode_username, session_id)

            # For now, just use GitHub data
            profile_data = github_data

    except Exception as e:
        print(f"Error scraping GitHub profile for {username}: {str(e)}")
        return {}

    return profile_data