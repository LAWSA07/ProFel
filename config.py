# config.py

# Original venue URLs for reference (commented out)
# BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-atlanta-ga"
# CSS_SELECTOR = "[class^='info-container']"
# REQUIRED_KEYS = [
#     "name",
#     "price",
#     "location",
#     "capacity",
#     "rating",
#     "reviews",
#     "description",
# ]

# User profiles to scrape
GITHUB_USERS = ["octocat"]  # Example GitHub username
LINKEDIN_USERS = []  # Add LinkedIn usernames here
LEETCODE_USERS = []  # Add LeetCode usernames here

# Job sites to scrape with their base URLs
JOB_SITES = [
    {"url": "https://www.indeed.com/jobs?q=software+engineer", "pages": 2},
    {"url": "https://www.linkedin.com/jobs/search/?keywords=software+engineer", "pages": 2},
]

# CSS selectors for different platforms
SELECTORS = {
    "github": {
        "profile": "div.application-main",
        "repos": "div#user-repositories-list",
    },
    "linkedin": {
        "profile": "div.profile-view-grid",
        "connections": "div.pv-profile-section",
    },
    "leetcode": {
        "profile": "div.content__Zt8k",
        "problems": "div.problems__Hm_q",
    },
    "jobs": {
        "indeed": "div.job_seen_beacon",
        "linkedin": "div.jobs-search-results-list",
    }
}

# Required fields for profiles and jobs
PROFILE_REQUIRED_KEYS = [
    "name",
    "skills",
]

JOB_REQUIRED_KEYS = [
    "title",
    "company",
    "description",
    "requirements",
]

# Matching thresholds
MATCH_THRESHOLDS = {
    "excellent": 85,
    "good": 70,
    "moderate": 50,
    "poor": 30,
}
