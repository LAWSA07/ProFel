from typing import Dict, Any, List
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com"

    async def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """Extract LinkedIn profile data"""
        profile_url = f"{self.base_url}/in/{username}"
        content = await self.retry_with_backoff(
            self.get_page_content, profile_url
        )

        soup = BeautifulSoup(content, 'html.parser')

        # Extract basic profile information
        profile_data = {
            'username': username,
            'name': self._extract_name(soup),
            'title': self._extract_title(soup),
            'location': self._extract_location(soup),
            'about': self._extract_about(soup),
            'experience': await self._extract_experience(soup),
            'education': await self._extract_education(soup),
            'skills': await self.extract_skills(soup),
            'certifications': await self._extract_certifications(soup),
            'projects': await self.extract_projects(soup),
            'recommendations': await self._extract_recommendations(soup)
        }

        return profile_data

    async def extract_skills(self, soup: BeautifulSoup) -> List[str]:
        """Extract skills from LinkedIn profile"""
        skills = set()

        # Extract from skills section
        skills_section = soup.select_one('section.skills-section')
        if skills_section:
            for skill in skills_section.select('span.skill-name'):
                skills.add(skill.text.strip())

        # Extract skills from experience descriptions
        for description in soup.select('.experience-section .description'):
            # Use regex to find tech terms in descriptions
            tech_terms = re.findall(r'\b(?:Python|JavaScript|React|Node\.js|SQL|Java|C\+\+|Ruby|Go|Rust|PHP|HTML|CSS|TypeScript|Angular|Vue\.js|Django|Flask|Spring|Express\.js|MongoDB|PostgreSQL|MySQL|Redis|Docker|Kubernetes|AWS|Azure|GCP|Git|CI/CD|REST|GraphQL|API|ML|AI|DevOps)\b', description.text)
            skills.update(tech_terms)

        # Extract from endorsements
        for endorsement in soup.select('.pv-skill-endorsement-entity'):
            skill_name = endorsement.select_one('.pv-skill-entity__skill-name')
            if skill_name:
                skills.add(skill_name.text.strip())

        return list(skills)

    async def extract_projects(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract projects from LinkedIn profile"""
        projects = []

        # Find projects section
        projects_section = soup.select_one('section#projects-section')
        if not projects_section:
            return projects

        # Extract individual projects
        for project in projects_section.select('li.project-item'):
            project_data = {
                'name': '',
                'description': '',
                'url': '',
                'date': ''
            }

            name_elem = project.select_one('.project-title')
            if name_elem:
                project_data['name'] = self._clean_text(name_elem.text)

            desc_elem = project.select_one('.project-description')
            if desc_elem:
                project_data['description'] = self._clean_text(desc_elem.text)

            url_elem = project.select_one('a.project-url')
            if url_elem:
                project_data['url'] = url_elem.get('href', '')

            date_elem = project.select_one('.project-date-range')
            if date_elem:
                project_data['date'] = self._clean_text(date_elem.text)

            projects.append(project_data)

        return projects

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract user's full name"""
        name_elem = soup.select_one('h1.text-heading-xlarge')
        return self._clean_text(name_elem.text) if name_elem else ''

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract user's professional title"""
        title_elem = soup.select_one('div.text-body-medium')
        return self._clean_text(title_elem.text) if title_elem else ''

    def _extract_location(self, soup: BeautifulSoup) -> str:
        """Extract user's location"""
        location_elem = soup.select_one('span.text-body-small')
        return self._clean_text(location_elem.text) if location_elem else ''

    def _extract_about(self, soup: BeautifulSoup) -> str:
        """Extract user's about section"""
        about_section = soup.select_one('section.about-section')
        if not about_section:
            return ''

        about_elem = about_section.select_one('div.display-flex')
        return self._clean_text(about_elem.text) if about_elem else ''

    async def _extract_experience(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract work experience"""
        experiences = []

        experience_section = soup.select_one('section#experience-section')
        if not experience_section:
            return experiences

        for position in experience_section.select('li.experience-item'):
            experience = {
                'title': '',
                'company': '',
                'location': '',
                'duration': '',
                'description': ''
            }

            title_elem = position.select_one('h3.t-16')
            if title_elem:
                experience['title'] = self._clean_text(title_elem.text)

            company_elem = position.select_one('p.pv-entity__secondary-title')
            if company_elem:
                experience['company'] = self._clean_text(company_elem.text)

            location_elem = position.select_one('.pv-entity__location span:nth-child(2)')
            if location_elem:
                experience['location'] = self._clean_text(location_elem.text)

            duration_elem = position.select_one('.pv-entity__date-range span:nth-child(2)')
            if duration_elem:
                experience['duration'] = self._clean_text(duration_elem.text)

            description_elem = position.select_one('.pv-entity__description')
            if description_elem:
                experience['description'] = self._clean_text(description_elem.text)

            experiences.append(experience)

        return experiences

    async def _extract_education(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract education history"""
        education_list = []

        education_section = soup.select_one('section#education-section')
        if not education_section:
            return education_list

        for school in education_section.select('li.education-item'):
            education = {
                'school': '',
                'degree': '',
                'field': '',
                'dates': '',
                'activities': ''
            }

            school_elem = school.select_one('h3.pv-entity__school-name')
            if school_elem:
                education['school'] = self._clean_text(school_elem.text)

            degree_elem = school.select_one('.pv-entity__degree-name .pv-entity__comma-item')
            if degree_elem:
                education['degree'] = self._clean_text(degree_elem.text)

            field_elem = school.select_one('.pv-entity__fos .pv-entity__comma-item')
            if field_elem:
                education['field'] = self._clean_text(field_elem.text)

            dates_elem = school.select_one('.pv-entity__dates span:nth-child(2)')
            if dates_elem:
                education['dates'] = self._clean_text(dates_elem.text)

            activities_elem = school.select_one('.activities-societies')
            if activities_elem:
                education['activities'] = self._clean_text(activities_elem.text)

            education_list.append(education)

        return education_list

    async def _extract_certifications(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract certifications"""
        certifications = []

        certifications_section = soup.select_one('section#certifications-section')
        if not certifications_section:
            return certifications

        for cert in certifications_section.select('li.certification-item'):
            certification = {
                'name': '',
                'issuer': '',
                'date': ''
            }

            name_elem = cert.select_one('h3.t-16')
            if name_elem:
                certification['name'] = self._clean_text(name_elem.text)

            issuer_elem = cert.select_one('p.pv-entity__secondary-title')
            if issuer_elem:
                certification['issuer'] = self._clean_text(issuer_elem.text)

            date_elem = cert.select_one('.pv-entity__date-range span:nth-child(2)')
            if date_elem:
                certification['date'] = self._clean_text(date_elem.text)

            certifications.append(certification)

        return certifications

    async def _extract_recommendations(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract recommendations"""
        recommendations = []

        recommendations_section = soup.select_one('section#recommendations-section')
        if not recommendations_section:
            return recommendations

        for rec in recommendations_section.select('li.recommendation-item'):
            recommendation = {
                'author': '',
                'relationship': '',
                'text': ''
            }

            author_elem = rec.select_one('.pv-recommendation-entity__detail h3')
            if author_elem:
                recommendation['author'] = self._clean_text(author_elem.text)

            relationship_elem = rec.select_one('.pv-recommendation-entity__detail p')
            if relationship_elem:
                recommendation['relationship'] = self._clean_text(relationship_elem.text)

            text_elem = rec.select_one('.pv-recommendation-entity__text')
            if text_elem:
                recommendation['text'] = self._clean_text(text_elem.text)

            recommendations.append(recommendation)

        return recommendations