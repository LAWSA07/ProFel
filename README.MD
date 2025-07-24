# Profel - AI-Powered Digital Profile Analyzer for Developers
### New Screenshot (2025-07-24)
![New Screenshot](images/Screenshot%202025-07-24%20121605.png)


## Problem Statement
In today's competitive job market, a strong digital presence is crucial for tech professionals. Recruiters evaluate candidates based on GitHub activity, LinkedIn engagement, and coding platform performance (LeetCode, CodeChef, CodeForces). However, manually assessing multiple profiles is time-consuming and inconsistent, lacking a standardized evaluation framework.

## The Challenge
- **Lack of visibility**: Developers struggle to understand how their profiles appear to recruiters.
- **No standardized evaluation**: No clear way to measure and compare technical skills across platforms.
- **Missing insights for improvement**: No guidance on how to enhance profiles for better career opportunities.

## Concept Overview
Profel is designed to create a system that takes a candidate's online profiles—like GitHub, LinkedIn, and LeetCode—and uses them to determine their technical skills. Using a smart language model, we extract keywords and technologies from those profiles and match them to job listings. The system then scores how well the candidate's skills fit each job opportunity.

## System Architecture

### 1. Frontend (User Interface)
- React-based web application with a modern, responsive design
- Simple forms for profile URL submission and job listing creation
- Real-time feedback and loading states
- Interactive dashboard for viewing matches and insights

### 2. Backend Processing Pipeline
- **Asynchronous Crawling**: Uses Crawl4AI for efficient multi-profile data collection
- **Data Processing**:
  - Text chunking for optimal processing
  - LLM-powered skill extraction
  - Vector embeddings generation
- **Storage**: Efficient database design for profiles, jobs, and matches
- **Matching Engine**: Sophisticated algorithm combining keyword matching and semantic similarity

## Key Features
- **Data Aggregation**: Automatically scrapes and verifies data from:
  - GitHub (repositories, contributions, README files)
  - LinkedIn (coming soon)
  - LeetCode (coming soon)
  - CodeForces (coming soon)
- **Profile Scoring**:
  - Analyzes coding contributions
  - Evaluates project diversity
  - Assesses problem-solving skills
  - Measures professional engagement
- **Insight Generation**:
  - Detailed strength/weakness analysis
  - Actionable recommendations
  - Skill gap identification
- **Recruiter Readiness Score**:
  - Hiring potential calculation
  - Profile optimization suggestions
  - Comparative analysis

## Technical Implementation

### Frontend Stack
- React.js for UI components
- TailwindCSS for styling
- React Router for navigation
- Local Storage for data persistence
- Spline for 3D background effects

### Backend Stack
- Python Flask backend
- Crawl4AI for asynchronous web scraping
- LLM integration (deepseek-r1-distill-llama-70b via Groq)
- Custom matching algorithms
- RESTful API design

## Project Structure
```
.
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── utils/         # Helper functions
│   │   └── App.js         # Main application component
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── backend/               # Python Flask backend
│   ├── app.py            # Main server file
│   ├── utils/            # Utility functions
│   │   ├── github_utils.py    # GitHub scraping utilities
│   │   └── matching_utils.py  # Profile-job matching utilities
│   └── requirements.txt   # Python dependencies
└── README.md             # Project documentation
```

## Screenshots

### Home Page
![Home Page](images/Screenshot%202025-04-03%20005314.png)

### GitHub Profile Analysis
![GitHub Profile Analysis](images/Screenshot%202025-04-03%20005321.png)

### Job Listing Form
![Job Listing Form](images/Screenshot%202025-04-03%20005334.png)

### Matching Results
![Matching Results](images/Screenshot%202025-04-03%20005341.png)

## Installation and Setup

### Prerequisites
- Node.js (v14 or higher)
- Python 3.12
- Git

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

### Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   conda create -n profel-env python=3.12 -y
   conda activate profel-env
   ```

2. Navigate to the backend directory:
   ```bash
   cd web-version/backend
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   python -m playwright install
   ```

5. Set up environment variables:
   Create a `.env` file with:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. Start the Flask server:
   ```bash
   python app.py
   ```

## Usage Guide

1. **Profile Submission**
   - Navigate to the Profiles page
   - Enter your GitHub username
   - Submit for analysis

2. **Job Listing Creation**
   - Go to the Jobs page
   - Fill in job details and required skills
   - Submit the listing

3. **View Matches**
   - Visit the Matching page
   - See your profile matches with job listings
   - Review detailed match scores and recommendations

## Future Enhancements
- Integration with LinkedIn API
- LeetCode profile analysis
- CodeForces rating integration
- Enhanced matching algorithms
- Machine learning-based skill predictions
- Automated profile improvement suggestions

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Crawl4AI for the web crawling framework
- Groq for LLM API access
- React community for frontend components
- All contributors and testers
