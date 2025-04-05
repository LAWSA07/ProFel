from typing import Dict, Any, List, Optional, Union
import logging
import numpy as np
from .text_processor import TextProcessor
from .embedding_generator import EmbeddingGenerator
from .database_manager import DatabaseManager

class MatchingEngine:
    """
    Engine for matching profiles against job listings using skills and vector similarity
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_processor = TextProcessor()
        self.embedding_generator = EmbeddingGenerator()
        self.db_manager = DatabaseManager()

        # Match importance weights
        self.weights = {
            'skill_overlap': 0.6,      # Exact skill match weight
            'vector_similarity': 0.4   # Semantic similarity weight
        }

    def process_profile(self, profile_data: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """
        Process a profile for matching (extract skills and generate embeddings)

        Args:
            profile_data: Profile data from scraper
            platform: Platform name (github, leetcode, etc.)

        Returns:
            Processed profile data with skills and embeddings
        """
        username = profile_data.get('username', '')

        # Extract text content for processing
        profile_text = self._extract_profile_text(profile_data, platform)

        # Process text to extract skills
        skills_data = self.text_processor.process_profile_text(profile_text['combined'])
        skills = skills_data.get('skills', [])

        # Generate embeddings for the profile sections
        embeddings = self.embedding_generator.generate_profile_embeddings(profile_text)

        # Store profile in database
        self.db_manager.store_profile(
            username=username,
            platform=platform,
            profile_data=profile_data,
            skills=skills,
            embedding=embeddings.get('overall')
        )

        return {
            'username': username,
            'platform': platform,
            'data': profile_data,
            'skills': skills,
            'embeddings': embeddings
        }

    def process_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a job for matching (extract skills and generate embeddings)

        Args:
            job_data: Job data with title, company, description, etc.

        Returns:
            Processed job data with skills and embeddings
        """
        title = job_data.get('title', '')
        company = job_data.get('company', '')
        description = job_data.get('description', '')

        # Extract skills from job description
        skills_text = description + " " + " ".join(job_data.get('skills', []))
        skills_data = self.text_processor.process_profile_text(skills_text)

        # Combine existing skills with extracted skills
        all_skills = set(job_data.get('skills', []))
        all_skills.update(skills_data.get('skills', []))
        skills = sorted(list(all_skills))

        # Generate embeddings for the job
        embeddings = self.embedding_generator.generate_job_embedding(description, skills)

        # Store job in database
        job_id = self.db_manager.store_job(
            title=title,
            company=company,
            description=description,
            skills=skills,
            embedding=embeddings.get('overall')
        )

        return {
            'id': job_id,
            'title': title,
            'company': company,
            'description': description,
            'skills': skills,
            'embeddings': embeddings
        }

    def match_profile_to_jobs(self, username: str, platform: str,
                            job_ids: List[int] = None) -> List[Dict[str, Any]]:
        """
        Match a profile against jobs

        Args:
            username: Profile username
            platform: Platform name
            job_ids: Optional list of job IDs to match against (otherwise all jobs)

        Returns:
            List of matches with scores
        """
        # Get profile from database
        profile = self.db_manager.get_profile(username, platform)
        if not profile:
            self.logger.error(f"Profile not found: {username} ({platform})")
            return []

        profile_skills = profile.get('skills', [])
        profile_embedding = profile.get('embedding')

        # Match against specified jobs or all jobs
        if job_ids:
            matches = []
            for job_id in job_ids:
                job = self.db_manager.get_job(job_id)
                if job:
                    match = self._match_profile_to_job(
                        profile_skills, profile_embedding, job
                    )
                    if match:
                        matches.append(match)
        else:
            # Find matching jobs from database
            matches = self.db_manager.find_matching_jobs(
                profile_embedding=profile_embedding,
                profile_skills=profile_skills
            )

        # Store matches in database
        for match in matches:
            self.db_manager.store_match(
                profile_id=profile.get('id'),
                job_id=match.get('id'),
                score=match.get('combined_score', 0),
                skill_overlap={
                    'matching_skills': match.get('skill_overlap', []),
                    'percentage': match.get('skill_overlap_pct', 0)
                }
            )

        return matches

    def _match_profile_to_job(self, profile_skills: List[str], profile_embedding: List[float],
                            job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Match a profile to a specific job"""
        job_id = job.get('id')
        job_skills = job.get('skills', [])
        job_embedding = job.get('embedding')

        # Calculate skill overlap
        matching_skills = set(profile_skills).intersection(set(job_skills))
        skill_overlap_pct = len(matching_skills) / len(job_skills) if job_skills else 0

        # Calculate vector similarity
        vector_similarity = 0
        if profile_embedding and job_embedding:
            vector_similarity = self.embedding_generator.cosine_similarity(
                profile_embedding, job_embedding
            )

        # Calculate combined score
        combined_score = (
            self.weights['skill_overlap'] * skill_overlap_pct +
            self.weights['vector_similarity'] * vector_similarity
        )

        return {
            'id': job_id,
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'description': job.get('description', ''),
            'skills': job_skills,
            'vector_similarity': vector_similarity,
            'skill_overlap': list(matching_skills),
            'skill_overlap_pct': skill_overlap_pct,
            'combined_score': combined_score
        }

    def _extract_profile_text(self, profile_data: Dict[str, Any], platform: str) -> Dict[str, str]:
        """Extract text content from profile data based on platform"""
        text_sections = {}

        if platform == 'github':
            # Extract from GitHub profile
            text_sections['bio'] = profile_data.get('bio', '')
            text_sections['name'] = profile_data.get('name', '')

            # Extract from repositories
            repos_text = []
            for repo in profile_data.get('repositories', []):
                repo_text = f"{repo.get('name', '')} - {repo.get('description', '')} ({repo.get('language', '')})"
                repos_text.append(repo_text)
            text_sections['repositories'] = "\n".join(repos_text)

            # Extract from projects
            projects_text = []
            for project in profile_data.get('projects', []):
                project_text = f"{project.get('name', '')} - {project.get('description', '')} ({project.get('language', '')})"
                projects_text.append(project_text)
            text_sections['projects'] = "\n".join(projects_text)

        elif platform == 'leetcode':
            # Extract from LeetCode profile
            profile_info = profile_data.get('profile', {})
            text_sections['bio'] = profile_info.get('aboutMe', '')
            text_sections['skills'] = ", ".join(profile_info.get('skillTags', []))

            # Extract submissions
            submissions = []
            for sub in profile_data.get('recent_submissions', []):
                submissions.append(f"{sub.get('title', '')} ({sub.get('lang', '')})")
            text_sections['submissions'] = "\n".join(submissions)

        elif platform == 'codeforces':
            # Extract from Codeforces profile
            info = profile_data.get('info', {})
            text_sections['bio'] = info.get('contribution', '')

            # Extract submissions
            submissions = []
            for sub in profile_data.get('submissions', [])[:20]:  # Limit to avoid too much text
                problem_name = sub.get('problem', {}).get('name', '')
                tags = sub.get('problem', {}).get('tags', [])
                lang = sub.get('programmingLanguage', '')
                submissions.append(f"{problem_name} ({lang}) - Tags: {', '.join(tags)}")
            text_sections['submissions'] = "\n".join(submissions)

        # Create combined text
        text_sections['combined'] = "\n\n".join(text_sections.values())

        return text_sections

    def calculate_match_score(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate match score between a profile and a job directly

        Args:
            profile: Profile data including skills and other attributes
            job: Job data including requirements and description

        Returns:
            Match score with details
        """
        try:
            # Extract skills
            profile_skills = self._extract_skills_from_profile(profile)
            job_skills = self._extract_skills_from_job(job)

            # Get text for similarity
            profile_text = self._get_profile_text_for_matching(profile)
            job_text = self._get_job_text_for_matching(job)

            # Generate embeddings if needed
            profile_embedding = self.embedding_generator.generate_text_embedding(profile_text)
            job_embedding = self.embedding_generator.generate_text_embedding(job_text)

            # Calculate skill overlap
            matching_skills = set(profile_skills).intersection(set(job_skills))
            missing_skills = set(job_skills) - set(profile_skills)

            skill_overlap_pct = len(matching_skills) / len(job_skills) if job_skills else 0

            # Calculate vector similarity
            vector_similarity = self.embedding_generator.cosine_similarity(
                profile_embedding, job_embedding
            ) if profile_embedding and job_embedding else 0.5

            # Calculate experience match (simple heuristic based on profile data)
            experience_match = self._calculate_experience_match(profile, job)

            # Calculate combined score
            combined_score = (
                self.weights['skill_overlap'] * skill_overlap_pct +
                self.weights['vector_similarity'] * vector_similarity
            )

            return {
                "overall_score": combined_score,
                "skill_match": skill_overlap_pct,
                "vector_similarity": vector_similarity,
                "experience_match": experience_match,
                "skills_matched": list(matching_skills),
                "skills_missing": list(missing_skills),
                "match_details": {
                    "profile_skills_count": len(profile_skills),
                    "job_skills_count": len(job_skills),
                    "matching_skills_count": len(matching_skills)
                }
            }

        except Exception as e:
            self.logger.error(f"Error in calculate_match_score: {str(e)}")
            # Return a default score
            return {
                "overall_score": 0.5,
                "skill_match": 0.5,
                "vector_similarity": 0.5,
                "experience_match": 0.5,
                "skills_matched": [],
                "skills_missing": [],
                "error": str(e)
            }

    def _extract_skills_from_profile(self, profile: Dict[str, Any]) -> List[str]:
        """Extract skills from profile data"""
        # Get skills directly if available
        if 'skills' in profile and isinstance(profile['skills'], list):
            return profile['skills']

        # Extract from profile data
        skills = []

        # If profile has data field (from backend)
        if 'data' in profile and isinstance(profile['data'], dict):
            profile_data = profile['data']
            if 'skills' in profile_data and isinstance(profile_data['skills'], list):
                skills.extend(profile_data['skills'])

        # Fallback: process text to extract skills
        if not skills:
            profile_text = self._get_profile_text_for_matching(profile)
            skills_data = self.text_processor.process_profile_text(profile_text)
            skills = skills_data.get('skills', [])

        return skills

    def _extract_skills_from_job(self, job: Dict[str, Any]) -> List[str]:
        """Extract skills from job data"""
        # Get skills directly if available
        if 'skills' in job and isinstance(job['skills'], list):
            return job['skills']

        # Extract from job description
        skills = []

        # Process text to extract skills
        job_text = self._get_job_text_for_matching(job)
        skills_data = self.text_processor.process_profile_text(job_text)
        skills = skills_data.get('skills', [])

        return skills

    def _get_profile_text_for_matching(self, profile: Dict[str, Any]) -> str:
        """Get text from profile data for matching"""
        text_parts = []

        # Handle different profile structures
        if 'data' in profile and isinstance(profile['data'], dict):
            profile_data = profile['data']
            text_parts.append(profile_data.get('bio', ''))
            text_parts.append(profile_data.get('description', ''))

            # Add repository descriptions
            for repo in profile_data.get('repositories', []):
                if isinstance(repo, dict):
                    text_parts.append(repo.get('description', ''))
                    text_parts.append(repo.get('language', ''))
        else:
            # Fallback to direct profile data
            text_parts.append(profile.get('bio', ''))
            text_parts.append(profile.get('description', ''))

        # Join all text parts
        return ' '.join(filter(None, text_parts))

    def _get_job_text_for_matching(self, job: Dict[str, Any]) -> str:
        """Get text from job data for matching"""
        text_parts = []

        text_parts.append(job.get('title', ''))
        text_parts.append(job.get('description', ''))

        # Add skills text if available
        skills = job.get('skills', [])
        if isinstance(skills, list):
            text_parts.append(' '.join(skills))
        elif isinstance(skills, str):
            text_parts.append(skills)

        # Join all text parts
        return ' '.join(filter(None, text_parts))

    def _calculate_experience_match(self, profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate experience match score based on profile and job data"""
        # Simple heuristic - can be expanded with actual logic
        return 0.7  # Default reasonable match

    def combine_profiles(self, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine multiple profiles from different platforms into a single profile

        Args:
            profiles: List of profiles from different platforms

        Returns:
            Combined profile data
        """
        if not profiles:
            return {}

        # Initialize the combined profile using the first profile as base
        combined_profile = {
            'id': 'combined_' + str(profiles[0].get('id', '')),
            'name': profiles[0].get('name', ''),
            'skills': [],
            'repositories': [],
            'projects': [],
            'experience': [],
            'education': [],
            'platforms': [],
            'certifications': []
        }

        all_skills = set()

        # Combine data from all profiles
        for profile in profiles:
            platform = profile.get('platform', 'unknown')
            combined_profile['platforms'].append(platform)

            # Extract skills from each profile
            profile_skills = self._extract_skills_from_profile(profile)
            all_skills.update(profile_skills)

            # Add platform-specific data
            if platform == 'github':
                # Add repositories from GitHub
                repos = profile.get('data', {}).get('repositories', [])
                combined_profile['repositories'].extend(repos)

            elif platform == 'linkedin':
                # Add experience from LinkedIn
                experience = profile.get('data', {}).get('experience', [])
                combined_profile['experience'].extend(experience)

                # Add education from LinkedIn
                education = profile.get('data', {}).get('education', [])
                combined_profile['education'].extend(education)

                # Add certifications from LinkedIn
                certifications = profile.get('data', {}).get('certifications', [])
                combined_profile['certifications'].extend(certifications)

            elif platform == 'leetcode':
                # Add problem-solving data from LeetCode
                solved_problems = profile.get('data', {}).get('solved_problems', {})
                if solved_problems:
                    combined_profile['problem_solving'] = solved_problems

                # Add recent submissions from LeetCode
                submissions = profile.get('data', {}).get('recent_submissions', [])
                if submissions:
                    combined_profile['submissions'] = submissions

            # Add projects from any platform
            projects = profile.get('data', {}).get('projects', [])
            combined_profile['projects'].extend(projects)

        # Update the combined skills list
        combined_profile['skills'] = list(all_skills)

        return combined_profile

    def match_combined_profile_to_job(self, profiles: List[Dict[str, Any]], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match combined profiles from multiple platforms to a job

        Args:
            profiles: List of profiles from different platforms
            job: Job data

        Returns:
            Match result with score and details
        """
        # Combine all profiles
        combined_profile = self.combine_profiles(profiles)

        # Calculate match using the combined profile
        match_result = self.calculate_match_score(combined_profile, job)

        # Add platform sources to the result
        match_result['platforms'] = combined_profile.get('platforms', [])
        match_result['profile_name'] = combined_profile.get('name', 'Combined Profile')

        # Add platform-specific contributions to the match
        platform_contributions = {}
        total_score = match_result.get('overall_score', 0)

        for platform in combined_profile.get('platforms', []):
            # Calculate approximate contribution of each platform
            if platform == 'github':
                platform_contributions[platform] = min(0.6, total_score * 0.5)  # Code/repos contribution
            elif platform == 'linkedin':
                platform_contributions[platform] = min(0.4, total_score * 0.3)  # Experience contribution
            elif platform == 'leetcode':
                platform_contributions[platform] = min(0.3, total_score * 0.2)  # Problem-solving contribution
            else:
                platform_contributions[platform] = 0

        match_result['platform_contributions'] = platform_contributions

        return match_result