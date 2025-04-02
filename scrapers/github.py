import asyncio
import time
from typing import Dict, List

from crawl4ai import AsyncWebCrawler

from config import SELECTORS
from models.profile import Skill, Project
from utils.scraper_utils import scrape_webpage, get_llm_strategy


# Maximum number of repositories to process
MAX_REPOS = 3
# Default wait time in seconds between retries
DEFAULT_RETRY_WAIT = 60
# Maximum number of retries for rate limit errors
MAX_RETRIES = 3


async def scrape_github_profile(
    crawler: AsyncWebCrawler,
    username: str,
    session_id: str
) -> Dict:
    """
    Scrape a GitHub profile.

    Args:
        crawler: The web crawler instance
        username: GitHub username
        session_id: Session identifier

    Returns:
        Dict: Extracted GitHub profile data
    """
    # GitHub profile URLs
    profile_url = f"https://github.com/{username}"
    repos_url = f"{profile_url}?tab=repositories"

    print(f"\nScraping GitHub profile for {username}...")

    # Define instruction for profile extraction with smaller scope
    profile_instruction = f"""
    Extract only the essential information from this GitHub profile page for user '{username}':
    1. Full name (if available) or use '{username}' if not found
    2. A brief bio or description (max 100 characters)
    3. Location (if available)
    4. Top 5-7 skills based on pinned repositories or language usage
    """

    # Define instruction for repositories extraction with limited scope
    repos_instruction = f"""
    Extract only the {MAX_REPOS} most recent or pinned projects from GitHub repositories for user '{username}' with:
    1. Project name
    2. Brief description (max 100 characters)
    3. Main technologies used (limit to 3-5 key technologies)
    4. Repository URL
    """

    # Create LLM strategies for different extraction tasks
    profile_strategy = get_llm_strategy(
        model_class=dict,  # Extract as raw dictionary first
        prompt_instruction=profile_instruction
    )

    repos_strategy = get_llm_strategy(
        model_class=dict,  # Extract as raw dictionary first
        prompt_instruction=repos_instruction
    )

    # Scrape profile data with retry logic
    profile_data = await scrape_with_retry(
        crawler,
        profile_url,
        SELECTORS["github"]["profile"],
        profile_strategy,
        session_id
    )

    # Handle case where profile_data is a list instead of a dict
    if isinstance(profile_data, list) and len(profile_data) > 0:
        # Use the first item if it's a list
        profile_data = profile_data[0] if isinstance(profile_data[0], dict) else {}
    elif not isinstance(profile_data, dict):
        profile_data = {}

    # Scrape repositories data with retry logic
    repos_data = await scrape_with_retry(
        crawler,
        repos_url,
        SELECTORS["github"]["repos"],
        repos_strategy,
        session_id
    )

    # Handle case where repos_data is a dict with a 'projects' key
    if isinstance(repos_data, dict) and "projects" in repos_data:
        repos_list = repos_data["projects"]
    # Handle case where repos_data is already a list
    elif isinstance(repos_data, list):
        repos_list = repos_data
    else:
        repos_list = []

    # Limit number of repositories to process
    repos_list = repos_list[:MAX_REPOS] if repos_list else []

    # Extract skills from profile data
    skills = []
    if "skills" in profile_data and isinstance(profile_data["skills"], list):
        # Limit skills to 10 to reduce data size
        for skill_name in profile_data.get("skills", [])[:10]:
            if isinstance(skill_name, str):
                skills.append({"name": skill_name})  # Use dict instead of Skill object
            elif isinstance(skill_name, dict) and "name" in skill_name:
                skills.append(skill_name)  # Keep as dict

    # Extract projects from repositories data
    projects = []
    for proj in repos_list:
        if isinstance(proj, dict) and "name" in proj:
            # Ensure technologies is a list
            if "technologies" in proj and not isinstance(proj["technologies"], list):
                proj["technologies"] = [proj["technologies"]]
            elif "technologies" not in proj:
                proj["technologies"] = []

            # Limit technologies to 5 to reduce data size
            if "technologies" in proj:
                proj["technologies"] = proj["technologies"][:5]

            # Keep as dict instead of Project object
            projects.append(proj)

    # Combine all data as dictionary (not Pydantic objects)
    github_info = {
        "name": profile_data.get("name", username),
        "bio": profile_data.get("bio", ""),
        "location": profile_data.get("location", ""),
        "skills": skills,  # List of skill dicts, not Skill objects
        "projects": projects,  # List of project dicts, not Project objects
        "github_stats": {
            "followers": profile_data.get("followers", 0),
            "following": profile_data.get("following", 0),
            "contributions": profile_data.get("contributions", 0),
            "stars": profile_data.get("stars", 0),
            "repositories": profile_data.get("repositories", 0),
        }
    }

    return github_info


async def scrape_with_retry(
    crawler: AsyncWebCrawler,
    url: str,
    css_selector: str,
    llm_strategy,
    session_id: str,
    retries: int = 0
) -> Dict:
    """
    Scrape webpage with retry logic for rate limits.

    Args:
        crawler: The web crawler instance
        url: URL to scrape
        css_selector: CSS selector for content
        llm_strategy: LLM extraction strategy
        session_id: Session identifier
        retries: Current retry count

    Returns:
        Dict: Extracted data
    """
    try:
        return await scrape_webpage(
            crawler,
            url,
            css_selector,
            llm_strategy,
            session_id
        )
    except Exception as e:
        error_str = str(e).lower()

        # Check if this is a rate limit error
        if retries < MAX_RETRIES and ("rate limit" in error_str or "too many requests" in error_str):
            # Calculate wait time with exponential backoff
            wait_time = DEFAULT_RETRY_WAIT * (2 ** retries)
            print(f"Rate limit reached. Waiting {wait_time} seconds before retry ({retries+1}/{MAX_RETRIES})...")

            await asyncio.sleep(wait_time)

            # Retry the request
            return await scrape_with_retry(
                crawler,
                url,
                css_selector,
                llm_strategy,
                session_id,
                retries + 1
            )
        else:
            # For other errors or if we've exhausted retries, return an empty dictionary
            print(f"Error scraping {url}: {e}")
            if retries >= MAX_RETRIES:
                print("Maximum retries reached. Continuing with partial data.")

            return {}