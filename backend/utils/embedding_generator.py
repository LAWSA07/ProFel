from typing import List, Dict, Any, Union
import os
import logging
import numpy as np
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class EmbeddingGenerator:
    """
    Generates vector embeddings for text using API services
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/embeddings"

        if not self.groq_api_key:
            self.logger.warning("GROQ_API_KEY not found in environment variables")

    def generate_embedding(self, text: str) -> Union[List[float], None]:
        """
        Generate a vector embedding for a piece of text

        Args:
            text: The text to generate an embedding for

        Returns:
            Vector embedding as a list of floats, or None if generation fails
        """
        if not self.groq_api_key:
            self.logger.error("Cannot generate embedding: GROQ_API_KEY not set")
            return None

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "embedding-001",
            "input": text,
            "encoding_format": "float"
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            embedding = result['data'][0]['embedding']
            return embedding

        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            return None

    def generate_embeddings_batch(self, texts: List[str]) -> List[Union[List[float], None]]:
        """
        Generate embeddings for a batch of texts

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embeddings (each as a list of floats), with None for failed generations
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Cosine similarity score (0-1)
        """
        if not embedding1 or not embedding2:
            return 0.0

        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def generate_profile_embeddings(self, profile_text: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate embeddings for different sections of a profile

        Args:
            profile_text: Dictionary with different sections of the profile
                        (e.g., 'bio', 'repositories', 'skills')

        Returns:
            Dictionary with embeddings for each section
        """
        embeddings = {}

        # Generate embeddings for each section
        for section, text in profile_text.items():
            if not text:
                continue

            embedding = self.generate_embedding(text)
            embeddings[section] = embedding

        # Generate an overall embedding for the combined text
        all_text = " ".join(profile_text.values())
        embeddings['overall'] = self.generate_embedding(all_text)

        return embeddings

    def generate_job_embedding(self, job_description: str, required_skills: List[str]) -> Dict[str, Any]:
        """
        Generate embeddings for a job listing

        Args:
            job_description: Full text of the job description
            required_skills: List of skills required for the job

        Returns:
            Dictionary with description and skills embeddings
        """
        embeddings = {}

        # Generate embedding for job description
        embeddings['description'] = self.generate_embedding(job_description)

        # Generate embedding for combined skills
        skills_text = ", ".join(required_skills)
        embeddings['skills'] = self.generate_embedding(skills_text)

        # Generate overall embedding
        all_text = job_description + " " + skills_text
        embeddings['overall'] = self.generate_embedding(all_text)

        return embeddings