# AI-Powered Digital Profile Analyzer for Developers

## Problem Statement
In today's competitive job market, a strong digital presence is crucial for tech professionals. Recruiters evaluate candidates based on GitHub activity, LinkedIn engagement, and coding platform performance (LeetCode, CodeChef, CodeForces). However, manually assessing multiple profiles is time-consuming and inconsistent, lacking a standardized evaluation framework.

## The Challenge
- **Lack of visibility**: Developers struggle to understand how their profiles appear to recruiters.
- **No standardized evaluation**: No clear way to measure and compare technical skills across platforms.
- **Missing insights for improvement**: No guidance on how to enhance profiles for better career opportunities.

## Key Features
Our AI-powered Digital Profile Analyzer:
- **Aggregates Data**: Automatically scrapes and verifies data from GitHub, LinkedIn, Codeforces and more coding platforms.
- **Profile Scoring**: Analyzes coding contributions, project diversity, problem-solving skills, and professional engagement.
- **Insight Generation**: Provides a detailed breakdown of strengths, weaknesses, and actionable recommendations.
- **Recruiter Readiness Score**: Generates a hiring potential score to help users optimize their digital presence.

## Screenshots

Here's how our application looks in action:

### Home Page
![Home Page](images/Screenshot%202025-04-03%20005314.png)

### GitHub Profile Analysis
![GitHub Profile Analysis](images/Screenshot%202025-04-03%20005321.png)

### Job Listing Form
![Job Listing Form](images/Screenshot%202025-04-03%20005334.png)

### Matching Results
![Matching Results](images/Screenshot%202025-04-03%20005341.png)

## Technical Implementation

This project is a Python tool that extracts professional profile data from GitHub and matches it against target job descriptions. It utilizes asynchronous programming with Crawl4AI and a language model-based extraction strategy (deepseek-r1-distill-llama-70b via Groq) to analyze a candidate's skills and match them with job requirements.

### Features

- Asynchronous web crawling using [Crawl4AI](https://pypi.org/project/Crawl4AI/)
- Data extraction powered by a language model (LLM) via Groq API
- Profile collection from GitHub (skills and repositories analysis)
- Target job matching with custom importance weights for skills
- Intelligent skill matching algorithm with score calculation
- JSON export of extracted data and match results
- Modular and easy-to-follow code structure
- Web interface for easy visualization and interaction

## Project Structure
```
.
├── main.py                  # Main entry point
├── config.py                # Configuration (selectors, etc.)
├── models/
│   ├── profile.py           # Profile data model
│   ├── job.py               # Job listing data model
│   └── match.py             # Match result data model
├── utils/
│   ├── data_utils.py        # Data processing utilities
│   ├── scraper_utils.py     # Scraping utilities
│   └── matching_utils.py    # Profile-job matching utilities
├── scrapers/
│   └── github.py            # GitHub scraper
├── web-version/             # Web application
│   ├── frontend/            # React frontend
│   └── backend/             # Python Flask backend
├── data/                    # Output directory for JSON files
├── requirements.txt         # Python package dependencies
├── .env                     # Environment variables (API keys)
└── README.MD                # This file
```

## Installation

1. **Create and Activate a Conda Environment**

   ```bash
   conda create -n deep-seek-crawler python=3.12 -y
   conda activate deep-seek-crawler
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**

   ```bash
   python -m playwright install
   ```

4. **Set Up Your Environment Variables**

   Create a `.env` file in the root directory with content similar to:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   *(Note: The `.env` file is in your .gitignore, so it won't be pushed to version control.)*

## Running the Command Line Version

To start the skill matcher, run:

```bash
python main.py
```

The script will:
1. Prompt you to enter GitHub usernames (comma-separated)
2. Prompt you to enter target job descriptions with required skills
3. Crawl the GitHub profiles to extract skills and project information
4. Match the profiles against the target job descriptions
5. Display match scores and save the results

### Input Format

For target job descriptions, use the following format:
```
<job_title> | <company> | <key_skills_comma_separated>
```

Example:
```
Senior Python Developer | Google | python,django,machine learning,sql
```

The skills listed first are considered more important for the matching algorithm.

## Running the Web Version

The web version provides a user-friendly interface for interacting with the tool.

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd web-version/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd web-version/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Output Files

The results are saved to the `data/` directory:
- `{username}_profile.json` - Individual profile data
- `job_listings.json` - Target job descriptions
- `profile_job_matches.json` - Match results with scores

## Configuration

The `config.py` file contains key constants used throughout the project:

- **SELECTORS**: CSS selectors for GitHub scraping
- **PROFILE_REQUIRED_KEYS**: Required fields for a valid profile
- **JOB_REQUIRED_KEYS**: Required fields for a valid job listing
- **MATCH_THRESHOLDS**: Thresholds for match quality categories

## Extending the Project

The project is designed to be easily extensible:

1. **Adding More Platforms**: Create new scraper modules for LinkedIn, LeetCode, etc. in the `scrapers/` directory
2. **Enhancing Match Algorithm**: Modify `utils/matching_utils.py` to improve matching logic
3. **Adding Output Formats**: Extend `utils/data_utils.py` to support additional output formats
4. **Expanding Web Interface**: Add more features to the React frontend

## Additional Notes

- **Rate Limiting**: The tool includes retry mechanisms with exponential backoff for handling API rate limits
- **Data Reduction**: The amount of data processed is limited to avoid hitting API limits
- **Error Handling**: Comprehensive error handling ensures the tool continues running even when some components fail
- **Local Storage**: The web version can function without a backend using localStorage for persistence

## License

MIT License
