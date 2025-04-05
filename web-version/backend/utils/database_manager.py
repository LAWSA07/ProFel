import os
import logging
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional, Union
import datetime

# Load environment variables
load_dotenv()

class DatabaseManager:
    """
    Manages database operations for storing profiles, jobs, and embeddings
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_url = os.getenv("DATABASE_URL")

        # Fallback to JSON storage if database URL not available
        self.use_json_fallback = not self.db_url
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

        if self.use_json_fallback:
            self.logger.warning("DATABASE_URL not found, using JSON file storage as fallback")
            os.makedirs(self.data_dir, exist_ok=True)
        else:
            self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist"""
        if not self.db_url:
            return

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Create extension for vector operations
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                    # Create profiles table
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS profiles (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        platform VARCHAR(50) NOT NULL,
                        data JSONB NOT NULL,
                        skills JSONB,
                        embedding_overall VECTOR(1536),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(username, platform)
                    );
                    """)

                    # Create jobs table
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS jobs (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        company VARCHAR(255) NOT NULL,
                        description TEXT NOT NULL,
                        skills JSONB NOT NULL,
                        embedding_overall VECTOR(1536),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """)

                    # Create matches table
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS matches (
                        id SERIAL PRIMARY KEY,
                        profile_id INTEGER REFERENCES profiles(id) ON DELETE CASCADE,
                        job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
                        score FLOAT NOT NULL,
                        skill_overlap JSONB NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(profile_id, job_id)
                    );
                    """)

                conn.commit()

        except Exception as e:
            self.logger.error(f"Database initialization error: {str(e)}")
            self.use_json_fallback = True

    def store_profile(self, username: str, platform: str, profile_data: Dict[str, Any],
                     skills: List[str] = None, embedding: List[float] = None) -> bool:
        """
        Store profile data in the database

        Args:
            username: Username of the profile
            platform: Platform name (github, leetcode, etc.)
            profile_data: Complete profile data dictionary
            skills: List of extracted skills
            embedding: Vector embedding of the profile (overall)

        Returns:
            Success status
        """
        if self.use_json_fallback:
            return self._store_profile_json(username, platform, profile_data, skills, embedding)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Check if profile exists
                    cur.execute(
                        "SELECT id FROM profiles WHERE username = %s AND platform = %s",
                        (username, platform)
                    )
                    result = cur.fetchone()

                    if result:
                        # Update existing profile
                        profile_id = result[0]
                        cur.execute(
                            """
                            UPDATE profiles
                            SET data = %s, skills = %s, embedding_overall = %s, updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (Json(profile_data), Json(skills) if skills else None,
                             embedding, profile_id)
                        )
                    else:
                        # Insert new profile
                        cur.execute(
                            """
                            INSERT INTO profiles (username, platform, data, skills, embedding_overall)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                            """,
                            (username, platform, Json(profile_data),
                             Json(skills) if skills else None, embedding)
                        )
                        profile_id = cur.fetchone()[0]

                    conn.commit()
                    return True

        except Exception as e:
            self.logger.error(f"Error storing profile: {str(e)}")
            return self._store_profile_json(username, platform, profile_data, skills, embedding)

    def _store_profile_json(self, username: str, platform: str, profile_data: Dict[str, Any],
                           skills: List[str] = None, embedding: List[float] = None) -> bool:
        """Store profile data in JSON file as fallback"""
        filename = f"{username}_{platform}_profile.json"
        file_path = os.path.join(self.data_dir, filename)

        # Create complete data structure
        complete_data = {
            "username": username,
            "platform": platform,
            "data": profile_data,
            "skills": skills,
            "embedding": embedding,
            "updated_at": str(datetime.datetime.now())
        }

        try:
            with open(file_path, 'w') as f:
                json.dump(complete_data, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Error storing profile as JSON: {str(e)}")
            return False

    def store_job(self, title: str, company: str, description: str,
                 skills: List[str], embedding: List[float] = None) -> Optional[int]:
        """
        Store job data in the database

        Args:
            title: Job title
            company: Company name
            description: Job description
            skills: Required skills for the job
            embedding: Vector embedding of the job (overall)

        Returns:
            Job ID if successful, None otherwise
        """
        if self.use_json_fallback:
            return self._store_job_json(title, company, description, skills, embedding)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO jobs (title, company, description, skills, embedding_overall)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (title, company, description, Json(skills), embedding)
                    )
                    job_id = cur.fetchone()[0]
                    conn.commit()
                    return job_id

        except Exception as e:
            self.logger.error(f"Error storing job: {str(e)}")
            return self._store_job_json(title, company, description, skills, embedding)

    def _store_job_json(self, title: str, company: str, description: str,
                       skills: List[str], embedding: List[float] = None) -> Optional[int]:
        """Store job data in JSON file as fallback"""
        jobs_file = os.path.join(self.data_dir, "jobs.json")

        # Load existing jobs or create new list
        try:
            if os.path.exists(jobs_file):
                with open(jobs_file, 'r') as f:
                    jobs = json.load(f)
            else:
                jobs = []

            # Generate a simple job ID
            job_id = len(jobs) + 1

            # Create job data
            job_data = {
                "id": job_id,
                "title": title,
                "company": company,
                "description": description,
                "skills": skills,
                "embedding": embedding,
                "created_at": str(datetime.datetime.now())
            }

            jobs.append(job_data)

            # Save updated jobs list
            with open(jobs_file, 'w') as f:
                json.dump(jobs, f, indent=2)

            return job_id

        except Exception as e:
            self.logger.error(f"Error storing job as JSON: {str(e)}")
            return None

    def store_match(self, profile_id: Union[int, str], job_id: Union[int, str],
                   score: float, skill_overlap: Dict[str, Any]) -> bool:
        """
        Store match between profile and job

        Args:
            profile_id: ID of the profile
            job_id: ID of the job
            score: Match score (0-1)
            skill_overlap: Dictionary with overlap details

        Returns:
            Success status
        """
        if self.use_json_fallback:
            return self._store_match_json(profile_id, job_id, score, skill_overlap)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Check if match already exists
                    cur.execute(
                        "SELECT id FROM matches WHERE profile_id = %s AND job_id = %s",
                        (profile_id, job_id)
                    )
                    result = cur.fetchone()

                    if result:
                        # Update existing match
                        match_id = result[0]
                        cur.execute(
                            """
                            UPDATE matches
                            SET score = %s, skill_overlap = %s, created_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (score, Json(skill_overlap), match_id)
                        )
                    else:
                        # Insert new match
                        cur.execute(
                            """
                            INSERT INTO matches (profile_id, job_id, score, skill_overlap)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (profile_id, job_id, score, Json(skill_overlap))
                        )

                    conn.commit()
                    return True

        except Exception as e:
            self.logger.error(f"Error storing match: {str(e)}")
            return self._store_match_json(profile_id, job_id, score, skill_overlap)

    def _store_match_json(self, profile_id: Union[int, str], job_id: Union[int, str],
                         score: float, skill_overlap: Dict[str, Any]) -> bool:
        """Store match data in JSON file as fallback"""
        matches_file = os.path.join(self.data_dir, "matches.json")

        # Load existing matches or create new list
        try:
            if os.path.exists(matches_file):
                with open(matches_file, 'r') as f:
                    matches = json.load(f)
            else:
                matches = []

            # Check if match already exists
            match_exists = False
            for i, match in enumerate(matches):
                if (str(match['profile_id']) == str(profile_id) and
                    str(match['job_id']) == str(job_id)):
                    # Update existing match
                    matches[i].update({
                        "score": score,
                        "skill_overlap": skill_overlap,
                        "created_at": str(datetime.datetime.now())
                    })
                    match_exists = True
                    break

            if not match_exists:
                # Create new match
                match_data = {
                    "id": len(matches) + 1,
                    "profile_id": profile_id,
                    "job_id": job_id,
                    "score": score,
                    "skill_overlap": skill_overlap,
                    "created_at": str(datetime.datetime.now())
                }
                matches.append(match_data)

            # Save updated matches list
            with open(matches_file, 'w') as f:
                json.dump(matches, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Error storing match as JSON: {str(e)}")
            return False

    def get_profile(self, username: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve profile data from database

        Args:
            username: Username of the profile
            platform: Platform name

        Returns:
            Profile data or None if not found
        """
        if self.use_json_fallback:
            return self._get_profile_json(username, platform)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, username, platform, data, skills, embedding_overall
                        FROM profiles
                        WHERE username = %s AND platform = %s
                        """,
                        (username, platform)
                    )
                    result = cur.fetchone()

                    if not result:
                        return None

                    return {
                        "id": result[0],
                        "username": result[1],
                        "platform": result[2],
                        "data": result[3],
                        "skills": result[4],
                        "embedding": result[5]
                    }

        except Exception as e:
            self.logger.error(f"Error retrieving profile: {str(e)}")
            return self._get_profile_json(username, platform)

    def _get_profile_json(self, username: str, platform: str) -> Optional[Dict[str, Any]]:
        """Retrieve profile from JSON file"""
        filename = f"{username}_{platform}_profile.json"
        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading profile from JSON: {str(e)}")
            return None

    def get_job(self, job_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Retrieve job data from database

        Args:
            job_id: ID of the job

        Returns:
            Job data or None if not found
        """
        if self.use_json_fallback:
            return self._get_job_json(job_id)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, title, company, description, skills, embedding_overall
                        FROM jobs
                        WHERE id = %s
                        """,
                        (job_id,)
                    )
                    result = cur.fetchone()

                    if not result:
                        return None

                    return {
                        "id": result[0],
                        "title": result[1],
                        "company": result[2],
                        "description": result[3],
                        "skills": result[4],
                        "embedding": result[5]
                    }

        except Exception as e:
            self.logger.error(f"Error retrieving job: {str(e)}")
            return self._get_job_json(job_id)

    def _get_job_json(self, job_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Retrieve job from JSON file"""
        jobs_file = os.path.join(self.data_dir, "jobs.json")

        if not os.path.exists(jobs_file):
            return None

        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)

            for job in jobs:
                if str(job['id']) == str(job_id):
                    return job

            return None

        except Exception as e:
            self.logger.error(f"Error reading job from JSON: {str(e)}")
            return None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Retrieve all job listings"""
        if self.use_json_fallback:
            return self._get_all_jobs_json()

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, title, company, description, skills, embedding_overall
                        FROM jobs
                        ORDER BY created_at DESC
                        """
                    )
                    results = cur.fetchall()

                    jobs = []
                    for row in results:
                        jobs.append({
                            "id": row[0],
                            "title": row[1],
                            "company": row[2],
                            "description": row[3],
                            "skills": row[4],
                            "embedding": row[5]
                        })

                    return jobs

        except Exception as e:
            self.logger.error(f"Error retrieving all jobs: {str(e)}")
            return self._get_all_jobs_json()

    def _get_all_jobs_json(self) -> List[Dict[str, Any]]:
        """Retrieve all jobs from JSON file"""
        jobs_file = os.path.join(self.data_dir, "jobs.json")

        if not os.path.exists(jobs_file):
            return []

        try:
            with open(jobs_file, 'r') as f:
                return json.load(f)

        except Exception as e:
            self.logger.error(f"Error reading all jobs from JSON: {str(e)}")
            return []

    def find_similar_profiles(self, embedding: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find profiles with similar embeddings using vector similarity

        Args:
            embedding: Vector embedding to compare against
            limit: Maximum number of results to return

        Returns:
            List of similar profiles with similarity scores
        """
        if self.use_json_fallback:
            return []  # Vector similarity search not available in JSON fallback mode

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, username, platform, data, skills,
                               1 - (embedding_overall <=> %s) AS similarity
                        FROM profiles
                        WHERE embedding_overall IS NOT NULL
                        ORDER BY similarity DESC
                        LIMIT %s
                        """,
                        (embedding, limit)
                    )
                    results = cur.fetchall()

                    profiles = []
                    for row in results:
                        profiles.append({
                            "id": row[0],
                            "username": row[1],
                            "platform": row[2],
                            "data": row[3],
                            "skills": row[4],
                            "similarity": row[5]
                        })

                    return profiles

        except Exception as e:
            self.logger.error(f"Error finding similar profiles: {str(e)}")
            return []

    def find_matching_jobs(self, profile_embedding: List[float], profile_skills: List[str],
                         limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find jobs matching a profile based on embedding similarity and skill overlap

        Args:
            profile_embedding: Vector embedding of the profile
            profile_skills: Skills from the profile
            limit: Maximum number of results to return

        Returns:
            List of matching jobs with scores
        """
        if self.use_json_fallback:
            return self._find_matching_jobs_json(profile_skills, limit)

        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # First get jobs with vector similarity
                    cur.execute(
                        """
                        SELECT id, title, company, description, skills,
                               1 - (embedding_overall <=> %s) AS similarity
                        FROM jobs
                        WHERE embedding_overall IS NOT NULL
                        ORDER BY similarity DESC
                        LIMIT %s
                        """,
                        (profile_embedding, limit * 2)  # Get more for filtering
                    )
                    results = cur.fetchall()

                    # Calculate skill overlap for each job
                    jobs_with_scores = []
                    for row in results:
                        job_id = row[0]
                        job_skills = row[4]
                        vector_similarity = row[5]

                        # Calculate skill overlap score
                        matching_skills = set(profile_skills).intersection(set(job_skills))
                        skill_overlap_pct = len(matching_skills) / len(job_skills) if job_skills else 0

                        # Combined score (50% vector similarity, 50% skill overlap)
                        combined_score = 0.5 * vector_similarity + 0.5 * skill_overlap_pct

                        jobs_with_scores.append({
                            "id": job_id,
                            "title": row[1],
                            "company": row[2],
                            "description": row[3],
                            "skills": job_skills,
                            "vector_similarity": vector_similarity,
                            "skill_overlap": list(matching_skills),
                            "skill_overlap_pct": skill_overlap_pct,
                            "combined_score": combined_score
                        })

                    # Sort by combined score and limit results
                    return sorted(jobs_with_scores,
                                 key=lambda x: x['combined_score'],
                                 reverse=True)[:limit]

        except Exception as e:
            self.logger.error(f"Error finding matching jobs: {str(e)}")
            return self._find_matching_jobs_json(profile_skills, limit)

    def _find_matching_jobs_json(self, profile_skills: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Find matching jobs based on skill overlap (fallback JSON implementation)"""
        jobs = self._get_all_jobs_json()

        # Calculate skill overlap for each job
        jobs_with_scores = []
        for job in jobs:
            job_skills = job.get('skills', [])

            # Calculate skill overlap
            matching_skills = set(profile_skills).intersection(set(job_skills))
            skill_overlap_pct = len(matching_skills) / len(job_skills) if job_skills else 0

            jobs_with_scores.append({
                "id": job['id'],
                "title": job['title'],
                "company": job['company'],
                "description": job['description'],
                "skills": job_skills,
                "vector_similarity": 0,  # Not available
                "skill_overlap": list(matching_skills),
                "skill_overlap_pct": skill_overlap_pct,
                "combined_score": skill_overlap_pct  # Only skill-based in fallback
            })

        # Sort by score and limit results
        return sorted(jobs_with_scores,
                     key=lambda x: x['combined_score'],
                     reverse=True)[:limit]