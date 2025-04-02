import json
import os
from typing import Dict, List, Set, Tuple, Type, Optional

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
from pydantic import BaseModel

from models.profile import Profile, Skill, Project, Certification, Connection
from models.job import JobListing, JobRequirement


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=False,  # Whether to run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
    )


def get_llm_strategy(model_class: Type[BaseModel], prompt_instruction: str) -> LLMExtractionStrategy:
    """
    Returns the configuration for the language model extraction strategy.

    Args:
        model_class: The Pydantic model class to use for extraction
        prompt_instruction: The instruction to give to the LLM

    Returns:
        LLMExtractionStrategy: The settings for how to extract data using LLM.
    """
    # https://docs.crawl4ai.com/api/strategies/#llmextractionstrategy

    # Handle dict type specially
    if model_class == dict:
        # Use a generic schema for dictionary extraction
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "bio": {"type": "string"},
                "location": {"type": "string"},
                "skills": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "projects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "technologies": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "url": {"type": "string"}
                        }
                    }
                },
                "jobs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "location": {"type": "string"},
                            "description": {"type": "string"},
                            "requirements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "skill": {"type": "string"},
                                        "importance": {"type": "number"}
                                    }
                                }
                            },
                            "salary_range": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    }
                }
            }
        }
    else:
        # Use the model's schema
        schema = model_class.model_json_schema()

    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",  # Name of the LLM provider
        api_token=os.getenv("GROQ_API_KEY"),  # API token for authentication
        schema=schema,  # JSON schema of the data model
        extraction_type="schema",  # Type of extraction to perform
        instruction=prompt_instruction,  # Instructions for the LLM
        input_format="markdown",  # Format of the input content
        verbose=True,  # Enable verbose logging
    )


async def scrape_webpage(
    crawler: AsyncWebCrawler,
    url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
) -> Dict:
    """
    Scrape a single webpage and return the extracted content

    Args:
        crawler: The web crawler instance
        url: The URL to scrape
        css_selector: The CSS selector to target content
        llm_strategy: The LLM extraction strategy
        session_id: Session identifier

    Returns:
        Dict: The extracted content
    """
    print(f"Scraping {url}...")

    # Fetch page content with the extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Do not use cached data
            extraction_strategy=llm_strategy,  # Strategy for data extraction
            css_selector=css_selector,  # Target specific content on the page
            session_id=session_id,  # Unique session ID for the crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching {url}: {result.error_message}")
        return {}

    try:
        # Parse extracted content
        extracted_data = json.loads(result.extracted_content)
        if not extracted_data:
            print(f"No data extracted from {url}.")
            return {}

        print(f"Successfully extracted data from {url}")
        return extracted_data
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {url}")
        return {}


async def check_pagination_end(
    crawler: AsyncWebCrawler,
    url: str,
    no_results_text: str,
    session_id: str,
) -> bool:
    """
    Checks if the pagination has reached the end.

    Args:
        crawler: The web crawler instance
        url: The URL to check
        no_results_text: Text that indicates no more results
        session_id: Session identifier

    Returns:
        bool: True if end of pagination, False otherwise
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if no_results_text in result.cleaned_html:
            return True
    else:
        print(f"Error checking pagination end: {result.error_message}")

    return False


async def is_complete_data(data: Dict, required_keys: List[str]) -> bool:
    """
    Checks if the data has all required keys.

    Args:
        data: The data to check
        required_keys: List of required keys

    Returns:
        bool: True if all required keys are present, False otherwise
    """
    return all(key in data for key in required_keys)


async def is_duplicate_data(identifier: str, seen_identifiers: Set[str]) -> bool:
    """
    Checks if the data with the given identifier has already been seen.

    Args:
        identifier: The unique identifier
        seen_identifiers: Set of identifiers already seen

    Returns:
        bool: True if duplicate, False otherwise
    """
    return identifier in seen_identifiers


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to check.
        session_id (str): The session identifier.

    Returns:
        bool: True if "No Results Found" message is found, False otherwise.
    """
    # Fetch the page without any CSS selector or extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "No Results Found" in result.cleaned_html:
            return True
    else:
        print(
            f"Error fetching page for 'No Results Found' check: {result.error_message}"
        )

    return False


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page of venue data.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        page_number (int): The page number to fetch.
        base_url (str): The base URL of the website.
        css_selector (str): The CSS selector to target the content.
        llm_strategy (LLMExtractionStrategy): The LLM extraction strategy.
        session_id (str): The session identifier.
        required_keys (List[str]): List of required keys in the venue data.
        seen_names (Set[str]): Set of venue names that have already been seen.

    Returns:
        Tuple[List[dict], bool]:
            - List[dict]: A list of processed venues from the page.
            - bool: A flag indicating if the "No Results Found" message was encountered.
    """
    url = f"{base_url}?page={page_number}"
    print(f"Loading page {page_number}...")

    # Check if "No Results Found" message is present
    no_results = await check_no_results(crawler, url, session_id)
    if no_results:
        return [], True  # No more results, signal to stop crawling

    # Fetch page content with the extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Do not use cached data
            extraction_strategy=llm_strategy,  # Strategy for data extraction
            css_selector=css_selector,  # Target specific content on the page
            session_id=session_id,  # Unique session ID for the crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page {page_number}: {result.error_message}")
        return [], False

    # Parse extracted content
    extracted_data = json.loads(result.extracted_content)
    if not extracted_data:
        print(f"No venues found on page {page_number}.")
        return [], False

    # After parsing extracted content
    print("Extracted data:", extracted_data)

    # Process venues
    complete_venues = []
    for venue in extracted_data:
        # Debugging: Print each venue to understand its structure
        print("Processing venue:", venue)

        # Ignore the 'error' key if it's False
        if venue.get("error") is False:
            venue.pop("error", None)  # Remove the 'error' key if it's False

        if not is_complete_venue(venue, required_keys):
            continue  # Skip incomplete venues

        if is_duplicate_venue(venue["name"], seen_names):
            print(f"Duplicate venue '{venue['name']}' found. Skipping.")
            continue  # Skip duplicate venues

        # Add venue to the list
        seen_names.add(venue["name"])
        complete_venues.append(venue)

    if not complete_venues:
        print(f"No complete venues found on page {page_number}.")
        return [], False

    print(f"Extracted {len(complete_venues)} venues from page {page_number}.")
    return complete_venues, False  # Continue crawling
