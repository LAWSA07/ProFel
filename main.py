import asyncio
import os
from typing import Dict, List
import json

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import (
    SELECTORS, PROFILE_REQUIRED_KEYS, JOB_REQUIRED_KEYS
)
from models.profile import Profile
from models.job import JobListing
from utils.data_utils import save_to_json, load_from_json
from utils.matching_utils import batch_match_profiles_to_jobs
from utils.scraper_utils import get_browser_config
from scrapers.github import scrape_github_profile
from scrapers.job_sites import scrape_job_listings

load_dotenv()


def get_user_input() -> tuple:
    """
    Get user input for GitHub usernames and target job descriptions.

    Returns:
        tuple: (github_usernames, target_jobs)
    """
    print("\n===== Deep Seek Profile Crawler and Job Matcher =====\n")

    # Get GitHub usernames
    github_input = input("Enter GitHub usernames (comma-separated): ").strip()
    raw_usernames = [username.strip() for username in github_input.split(",") if username.strip()]

    # Process GitHub usernames to extract from URLs if needed
    github_usernames = []
    for raw_username in raw_usernames:
        # Check if it's a URL and extract the username
        if "github.com/" in raw_username:
            # Extract username from URL
            parts = raw_username.split("github.com/")
            if len(parts) > 1:
                username = parts[1].strip().split("/")[0].split("?")[0]
                github_usernames.append(username)
                print(f"Extracted username '{username}' from URL: {raw_username}")
            else:
                print(f"Couldn't parse username from URL: {raw_username}")
        else:
            # It's already a username
            github_usernames.append(raw_username)

    if not github_usernames:
        github_usernames = ["octocat"]  # Default if no input
        print(f"Using default GitHub username: {github_usernames[0]}")

    # Get target job descriptions
    print("\nEnter target job descriptions (leave empty to finish):")
    print("Format: <job_title> | <company> | <key_skills_comma_separated>")
    print("Example: Senior Python Developer | Google | python,django,machine learning,sql")

    target_jobs = []
    while True:
        job_input = input("> ").strip()
        if not job_input:
            break

        parts = job_input.split("|")
        if len(parts) >= 3:
            title = parts[0].strip()
            company = parts[1].strip()
            skills_text = parts[2].strip()

            # Process skills and assign importance
            skills = []
            for i, skill in enumerate(skills_text.split(",")):
                skill = skill.strip()
                if skill:
                    # Assign higher importance to skills listed first
                    importance = max(0.3, 1.0 - (i * 0.1))
                    skills.append({
                        "skill": skill,
                        "importance": round(importance, 1)
                    })

            job = {
                "title": title,
                "company": company,
                "location": parts[3].strip() if len(parts) > 3 else "Not specified",
                "description": f"Custom job description for {title} at {company}",
                "requirements": skills,
                "url": "",  # No URL for manually entered jobs
            }

            target_jobs.append(job)
            print(f"Added job: {title} at {company} with {len(skills)} skills")
        else:
            print("Invalid format. Please use: <job_title> | <company> | <key_skills_comma_separated>")

    # Use a default example job if none provided
    if not target_jobs:
        default_jobs = [
            {
                "title": "Software Engineer",
                "company": "Example Tech",
                "location": "Remote",
                "description": "Software engineering position focusing on backend development",
                "requirements": [
                    {"skill": "Python", "importance": 1.0},
                    {"skill": "JavaScript", "importance": 0.8},
                    {"skill": "SQL", "importance": 0.7},
                    {"skill": "Git", "importance": 0.6},
                    {"skill": "REST API", "importance": 0.5},
                ],
                "url": ""
            }
        ]
        target_jobs = default_jobs
        print("\nUsing default example job:")
        for job in default_jobs:
            skills = [req["skill"] for req in job["requirements"]]
            print(f"  - {job['title']} at {job['company']}: {', '.join(skills)}")

    return github_usernames, target_jobs


async def build_profile(username: str) -> Dict:
    """
    Build a user profile from GitHub data.

    Args:
        username: The GitHub username

    Returns:
        Dict: The profile data
    """
    print(f"Building profile for {username}...")

    # Initialize browser configuration
    browser_config = get_browser_config()
    session_id = f"profile_{username}"

    # Initialize profile data
    profile_data = {}

    # Start the web crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Scrape GitHub profile
        github_data = await scrape_github_profile(crawler, username, session_id)

        # In the future, add LinkedIn and LeetCode scrapers
        # linkedin_data = await scrape_linkedin_profile(crawler, linkedin_username, session_id)
        # leetcode_data = await scrape_leetcode_profile(crawler, leetcode_username, session_id)

        # For now, just use GitHub data
        profile_data = github_data

    return profile_data


async def scrape_jobs(target_jobs: List[Dict]) -> List[Dict]:
    """
    Process target job descriptions.

    Args:
        target_jobs: List of manually entered target job descriptions

    Returns:
        List[Dict]: List of job listings
    """
    print("\nProcessing target job descriptions...")

    # The target jobs are already in the right format, just return them
    print(f"Processed {len(target_jobs)} target job descriptions")

    return target_jobs


async def main():
    """
    Main function to run the profile crawler and job matcher.

    Workflow:
    1. Get GitHub usernames and target job descriptions from user input
    2. Scrape GitHub profiles for skills and projects
    3. Match profiles against the target job descriptions
    4. Save results and display match scores
    """
    try:
        # Get user input
        github_usernames, target_jobs = get_user_input()

        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Step 1: Build profiles from GitHub
        profiles_data = []
        for username in github_usernames:
            try:
                profile_data = await build_profile(username)

                # Validate profile data
                if not all(key in profile_data for key in PROFILE_REQUIRED_KEYS):
                    print(f"Warning: Profile for {username} is missing required fields")
                    continue

                profiles_data.append(profile_data)

                # Save individual profile
                save_to_json(profile_data, f"data/{username}_profile.json")
                print(f"Successfully saved profile for {username}")
            except Exception as e:
                print(f"Error processing profile for {username}: {e}")
                continue

        # Convert to Profile objects
        profiles = []
        for data in profiles_data:
            try:
                # Create a Profile object with lists of dictionaries instead of Pydantic objects
                profile_args = data.copy()

                # Handle skill objects - keep as dictionaries
                if "skills" in profile_args and isinstance(profile_args["skills"], list):
                    # Skills are already dictionaries from our modified scraper
                    pass

                # Handle project objects - keep as dictionaries
                if "projects" in profile_args and isinstance(profile_args["projects"], list):
                    # Projects are already dictionaries from our modified scraper
                    pass

                profile = Profile(**profile_args)
                profiles.append(profile)
            except Exception as e:
                print(f"Error creating Profile object: {e}")

        # Step 2: Process target job descriptions (no scraping needed)
        try:
            jobs_data = await scrape_jobs(target_jobs)

            # Save all job listings
            save_to_json(jobs_data, "data/job_listings.json")
            print(f"Successfully saved {len(jobs_data)} target job descriptions to data/job_listings.json")
        except Exception as e:
            print(f"Error processing target job descriptions: {e}")
            jobs_data = []

        # Convert to JobListing objects
        jobs = []
        for data in jobs_data:
            try:
                # Create JobListing objects from dictionaries
                job_args = data.copy()

                # Make sure requirements is a list of JobRequirement objects
                if "requirements" in job_args and isinstance(job_args["requirements"], list):
                    requirements = []
                    for req in job_args["requirements"]:
                        if isinstance(req, dict) and "skill" in req:
                            requirements.append(JobRequirement(**req))
                    job_args["requirements"] = requirements

                job = JobListing(**job_args)
                jobs.append(job)
            except Exception as e:
                print(f"Error creating JobListing object: {e}")

        # Step 3: Match profiles to jobs
        if profiles and jobs:
            try:
                print("\nMatching profiles to target jobs...")
                matches = await batch_match_profiles_to_jobs(profiles, jobs)

                # Save matching results
                save_to_json(matches, "data/profile_job_matches.json")
                print(f"Successfully saved match results to data/profile_job_matches.json")

                # Print summary of matches
                for profile_match in matches:
                    profile_name = profile_match["profile_name"]
                    top_matches = profile_match["matches"]

                    print(f"\nMatches for {profile_name}:")
                    for i, match in enumerate(top_matches, 1):
                        print(f"  {i}. {match['job_title']} at {match['company']} - {match['overall_match']:.1f}% match")
                        print(f"     Recommendation: {match['recommendation']}")
                        if match['strengths']:
                            print(f"     Strengths: {', '.join(match['strengths'][:3])}")
                        if match['missing_skills']:
                            print(f"     Missing skills: {', '.join(match['missing_skills'][:3])}")
            except Exception as e:
                print(f"Error matching profiles to jobs: {e}")
        else:
            print("\nNo profiles or jobs to match")

        print("\nProcess completed! Results saved to the 'data' directory.")

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        print("The program will try to save any data collected so far.")
        # Try to create the data directory if it doesn't exist
        try:
            os.makedirs("data", exist_ok=True)
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
