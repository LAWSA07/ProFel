from typing import List, Dict, Any
import re
import os
import logging
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TextProcessor:
    """
    Handles text chunking and LLM processing for skill extraction
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        if not self.groq_api_key:
            self.logger.warning("GROQ_API_KEY not found in environment variables")

    def chunk_text(self, text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks to preserve context

        Args:
            text: The text to chunk
            max_chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks

        Returns:
            List of text chunks
        """
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)

        # Remove multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # If paragraph is too long, split it by sentences
            if len(paragraph) > max_chunk_size:
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) <= max_chunk_size:
                        current_chunk += sentence + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + " "
            else:
                # Check if adding this paragraph exceeds the max chunk size
                if len(current_chunk) + len(paragraph) <= max_chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())

        # Handle overlap between chunks
        if overlap > 0 and len(chunks) > 1:
            overlapped_chunks = [chunks[0]]
            for i in range(1, len(chunks)):
                previous_chunk = chunks[i-1]
                current_chunk = chunks[i]

                # Get overlap from previous chunk
                if len(previous_chunk) > overlap:
                    overlap_text = previous_chunk[-overlap:]
                    current_with_overlap = overlap_text + current_chunk
                    overlapped_chunks.append(current_with_overlap)
                else:
                    overlapped_chunks.append(current_chunk)

            return overlapped_chunks

        return chunks

    def extract_skills_with_llm(self, text: str) -> List[str]:
        """
        Use LLM to extract technical skills from text

        Args:
            text: The text to extract skills from

        Returns:
            List of extracted skills
        """
        if not self.groq_api_key:
            self.logger.error("Cannot extract skills: GROQ_API_KEY not set")
            return []

        prompt = f"""
        Analyze the following text and extract ALL technical skills, programming languages, frameworks, tools, and technologies mentioned.
        Return ONLY a JSON array of strings with the skills, nothing else.

        Text to analyze:
        {text}
        """

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are a skilled assistant that extracts technical skills from text. You ONLY return a JSON array of strings, nothing else."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 1024
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            response_data = response.json()
            content = response_data['choices'][0]['message']['content']

            # Extract JSON array from the response
            skills_match = re.search(r'\[.*\]', content, re.DOTALL)
            if skills_match:
                skills_json = skills_match.group()
                skills = json.loads(skills_json)
                return skills

            # If regex didn't work, try direct JSON parsing
            try:
                skills = json.loads(content)
                if isinstance(skills, list):
                    return skills
            except json.JSONDecodeError:
                pass

            self.logger.warning(f"Could not parse skills from LLM response: {content}")
            return []

        except Exception as e:
            self.logger.error(f"Error extracting skills with LLM: {str(e)}")
            return []

    def process_profile_text(self, text: str) -> Dict[str, Any]:
        """
        Process profile text through chunking and LLM extraction

        Args:
            text: The profile text to process

        Returns:
            Dictionary with extracted skills and metadata
        """
        chunks = self.chunk_text(text)

        all_skills = set()
        for chunk in chunks:
            skills = self.extract_skills_with_llm(chunk)
            all_skills.update(skills)

        return {
            "skills": sorted(list(all_skills)),
            "chunk_count": len(chunks)
        }