import asyncio
from typing import Dict, List

from crawl4ai import AsyncWebCrawler

from config import SELECTORS, JOB_REQUIRED_KEYS
from models.job import JobListing, JobRequirement
from utils.scraper_utils import scrape_webpage, get_llm_strategy, is_complete_data, is_duplicate_data

# Maximum jobs to collect per site
MAX_JOBS_PER_SITE = 5
# Default wait time in seconds between retries
DEFAULT_RETRY_WAIT = 60
# Maximum number of retries for rate limit errors
MAX_RETRIES = 3


async def scrape_job_listings(
    crawler: AsyncWebCrawler,
    site_config: Dict,
    session_id: str
) -> List[Dict]:
    """
    Scrape job listings from a job site.

    Args:
        crawler: The web crawler instance
        site_config: Configuration for the job site
        session_id: Session identifier

    Returns:
        List[Dict]: List of job listings
    """
    base_url = site_config["url"]
    pages = min(site_config.get("pages", 1), 2)  # Limit to 2 pages max to reduce data
    site_name = get_site_name(base_url)

    jobs = []
    seen_job_titles = set()

    # Define instruction for job extraction with reduced scope
    job_instruction = """
    Extract the top 5 most relevant job listings with only these key fields:
    1. Job title
    2. Company name
    3. Job location
    4. Brief job description (max 100 characters)
    5. 3-5 most important required skills and their importance (on a scale of 0-1)
    6. Salary range (if available)
    7. Job URL
    """

    # Create LLM strategy for job extraction
    job_strategy = get_llm_strategy(
        model_class=dict,  # Extract as raw dictionary first
        prompt_instruction=job_instruction
    )

    # Define selector based on the site
    if "indeed" in base_url.lower():
        css_selector = SELECTORS["jobs"]["indeed"]
    elif "linkedin" in base_url.lower():
        css_selector = SELECTORS["jobs"]["linkedin"]
    else:
        css_selector = "div.job-listing"  # Generic fallback

    # Scrape each page
    for page in range(1, pages + 1):
        page_url = f"{base_url}&start={(page-1)*10}" if "indeed" in base_url.lower() else f"{base_url}&page={page}"

        print(f"\nScraping jobs from {page_url} (page {page}/{pages})...")

        # Scrape job listings from the page with retry logic
        try:
            page_jobs_data = await scrape_with_retry(
                crawler,
                page_url,
                css_selector,
                job_strategy,
                f"{session_id}_{site_name}_page{page}"
            )
        except Exception as e:
            print(f"Error scraping jobs from {page_url}: {e}")
            continue

        # Process job listings
        if isinstance(page_jobs_data, dict) and "jobs" in page_jobs_data:
            page_jobs = page_jobs_data.get("jobs", [])
        elif isinstance(page_jobs_data, list):
            page_jobs = page_jobs_data
        else:
            page_jobs = []

        for job in page_jobs:
            if not job or not isinstance(job, dict):
                continue

            # Check if job has all required fields
            if not await is_complete_data(job, JOB_REQUIRED_KEYS):
                continue

            # Check for duplicates
            job_identifier = f"{job['title']}_{job['company']}"
            if await is_duplicate_data(job_identifier, seen_job_titles):
                continue

            # Process requirements
            if "requirements" in job:
                processed_requirements = []
                for req in job["requirements"]:
                    if isinstance(req, dict) and "skill" in req:
                        # Ensure importance is a float between 0 and 1
                        if "importance" not in req:
                            req["importance"] = 0.5
                        elif not isinstance(req["importance"], (int, float)):
                            req["importance"] = 0.5
                        elif req["importance"] > 1:
                            req["importance"] = 1.0
                        elif req["importance"] < 0:
                            req["importance"] = 0.0

                        processed_requirements.append(req)
                    elif isinstance(req, str):
                        processed_requirements.append({"skill": req, "importance": 0.5})

                job["requirements"] = processed_requirements

            # Add job URL if missing
            if "url" not in job:
                job["url"] = page_url

            seen_job_titles.add(job_identifier)
            jobs.append(job)

            # Limit the number of jobs to reduce data
            if len(jobs) >= MAX_JOBS_PER_SITE:
                print(f"Reached maximum of {MAX_JOBS_PER_SITE} jobs for {site_name}. Stopping.")
                break

        # Stop if we've collected enough jobs
        if len(jobs) >= MAX_JOBS_PER_SITE:
            break

        # Be polite and avoid rate limiting
        await asyncio.sleep(2)

    print(f"Scraped {len(jobs)} jobs from {site_name}")
    return jobs


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


def get_site_name(url: str) -> str:
    """Extract site name from URL"""
    if "indeed" in url.lower():
        return "indeed"
    elif "linkedin" in url.lower():
        return "linkedin"
    else:
        return "job_site"