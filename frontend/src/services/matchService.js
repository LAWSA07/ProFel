import api from './api';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Get all match results
 * @returns {Promise<Array>} Array of match results
 */
export const getAllMatches = async () => {
  try {
    const response = await api.get('/match');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching matches:', error);
    throw error;
  }
};

/**
 * Get a specific match result
 * @param {string} matchId - Match ID
 * @returns {Promise<Object>} Match result data
 */
export const getMatch = async (matchId) => {
  try {
    const response = await api.get(`/match/${matchId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching match ${matchId}:`, error);
    throw error;
  }
};

/**
 * Match a profile to a job
 * @param {string} profileId - Profile ID or username
 * @param {string} jobId - Job ID
 * @returns {Promise<Object>} Match result data
 */
export const matchProfileToJob = async (profileId, jobId) => {
  try {
    const response = await api.post('/match/calculate', { profile_id: profileId, job_id: jobId });
    return response.data;
  } catch (error) {
    console.error(`Error matching profile ${profileId} to job ${jobId}:`, error);
    throw error;
  }
};

/**
 * Get all matches for a specific profile
 * @param {string} profileId - Profile ID or username
 * @returns {Promise<Array>} Array of match results
 */
export const getProfileMatches = async (profileId) => {
  try {
    const response = await api.get(`/match/profile/${profileId}`);
    return response.data || [];
  } catch (error) {
    console.error(`Error fetching matches for profile ${profileId}:`, error);
    throw error;
  }
};

/**
 * Get all matches for a specific job
 * @param {string} jobId - Job ID
 * @returns {Promise<Array>} Array of match results
 */
export const getJobMatches = async (jobId) => {
  try {
    const response = await api.get(`/match/job/${jobId}`);
    return response.data || [];
  } catch (error) {
    console.error(`Error fetching matches for job ${jobId}:`, error);
    throw error;
  }
};

/**
 * Delete a match result
 * @param {string} matchId - Match ID
 * @returns {Promise<Object>} Response data
 */
export const deleteMatch = async (matchId) => {
  try {
    const response = await api.delete(`/match/${matchId}`);
    return response;
  } catch (error) {
    console.error(`Error deleting match ${matchId}:`, error);
    throw error;
  }
};

/**
 * Calculate match score between a profile and job
 * @param {Object} profile - Profile object with skills
 * @param {Object} job - Job object with skills
 * @returns {Promise<Object>} Match result with score
 */
export const calculateMatch = async (profile, job) => {
  try {
    console.log('calculateMatch: Processing match', { profile, job });

    // If job has a description but no skills, extract skills from description
    if (job.description && (!job.skills || !job.skills.length)) {
      console.log('Extracting skills from job description');
      const techKeywords = extractTechKeywords(job.description);
      job.skills = techKeywords;
      console.log('Extracted job skills:', job.skills);
    }

    // Always use local calculation for now until backend is fixed
    const result = performLocalMatch(profile, job);

    console.log('calculateMatch: Used local calculation', result);
    return result;

    // Commented out API call due to CORS issues
    /*
    const response = await axios.post(`${API_URL}/match/calculate`, {
      profile,
      job
    });
    console.log('calculateMatch: Received response', response.data);
    return response.data;
    */
  } catch (error) {
    console.error('Error calculating match:', error);
    // Return default score if API fails
    return {
      overall_score: 0.5,
      skill_match: 0.5,
      skills_matched: [],
      skills_missing: [],
      error: error.message
    };
  }
};

/**
 * Calculate match score using multiple combined profiles
 * @param {Array} profiles - Array of profile objects
 * @param {Object} job - Job object with skills
 * @returns {Promise<Object>} Match result with score
 */
export const calculateCombinedMatch = async (profiles, job) => {
  try {
    console.log('calculateCombinedMatch: Using profiles', { profiles, job });

    // If job has a description but no skills, extract skills from description
    if (job.description && (!job.skills || !job.skills.length)) {
      console.log('Extracting skills from job description');
      const techKeywords = extractTechKeywords(job.description);
      job.skills = techKeywords;
      console.log('Extracted job skills:', job.skills);
    }

    // Extract all skills from all profiles
    const allProfileSkills = [];
    profiles.forEach(profile => {
      const skills = extractSkills(profile);
      console.log(`Extracted skills from ${profile.platform || 'unknown'} profile:`, skills);
      allProfileSkills.push(...skills);
    });

    // Deduplicate skills
    const uniqueSkills = [...new Set(allProfileSkills)];
    console.log('Combined unique skills:', uniqueSkills);

    const profileObj = { skills: uniqueSkills };
    const result = performLocalMatch(profileObj, job);

    // Add platforms to result
    result.platforms = profiles.map(p => p.platform).filter(Boolean);

    console.log('calculateCombinedMatch: Result', result);
    return result;

    // Commented out API call due to CORS issues
    /*
    const response = await axios.post(`${API_URL}/match/calculate-combined`, {
      profiles,
      job
    });
    console.log('calculateCombinedMatch: Received response', response.data);
    return response.data;
    */
  } catch (error) {
    console.error('Error calculating combined match:', error);
    // Return default score if API fails
    return {
      overall_score: 0.5,
      skill_match: 0.5,
      skills_matched: [],
      skills_missing: [],
      platforms: profiles.map(p => p.platform).filter(Boolean),
      error: error.message
    };
  }
};

/**
 * Combine multiple profiles from different platforms
 * @param {Array} profiles - Array of profile objects from different platforms
 * @returns {Promise<Object>} Combined profile
 */
export const combineProfiles = async (profiles) => {
  try {
    console.log('combineProfiles: Sending request to API', { profiles });
    const response = await axios.post(`${API_URL}/profile/combine`, {
      profiles
    });
    console.log('combineProfiles: Received response', response.data);
    return response.data;
  } catch (error) {
    console.error('Error combining profiles:', error);
    return {
      error: error.message,
      profiles_count: profiles.length
    };
  }
};

/**
 * Manual matching function that can be used if API is not available
 * This is a fallback calculation that doesn't rely on backend services
 */
export const performLocalMatch = (profile, job) => {
  console.log('performLocalMatch: Performing local calculation', { profile, job });

  // Extract skills with better logging
  const profileSkills = extractSkills(profile);
  const jobSkills = extractSkills(job);

  console.log('Extracted profile skills:', profileSkills);
  console.log('Extracted job skills:', jobSkills);

  // Always ensure we have at least some skills to compare
  // If no job skills, use a basic set of expected skills based on job title
  const effectiveJobSkills = jobSkills.length > 0 ?
    jobSkills :
    ['communication', 'teamwork', 'problem solving', 'professional'];

  // Default value if no profile skills to match
  if (!profileSkills.length) {
    return {
      overall_score: 0.3,
      skill_match: 0.3,
      skills_matched: [],
      skills_missing: effectiveJobSkills,
      message: "No profile skills found for matching"
    };
  }

  // Find matching skills (case insensitive)
  const matchedSkills = [];
  const similarityThreshold = 0.6; // Threshold for skill similarity (0.0 to 1.0)

  profileSkills.forEach(pSkill => {
    // Find the best match from job skills
    const bestMatch = effectiveJobSkills.find(jSkill =>
      calculateStringSimilarity(pSkill.toLowerCase(), jSkill.toLowerCase()) >= similarityThreshold
    );

    if (bestMatch && !matchedSkills.includes(pSkill)) {
      matchedSkills.push(pSkill);
    }
  });

  // Find missing skills
  const missingSkills = effectiveJobSkills.filter(jSkill =>
    !profileSkills.some(pSkill =>
      calculateStringSimilarity(pSkill.toLowerCase(), jSkill.toLowerCase()) >= similarityThreshold
    )
  );

  // Calculate match percentage
  const score = effectiveJobSkills.length > 0 ?
    matchedSkills.length / effectiveJobSkills.length : 0.5;

  // Ensure the score is a valid number between 0 and 1
  const validScore = isNaN(score) ? 0.5 : Math.max(0, Math.min(1, score));

  return {
    overall_score: validScore,
    skill_match: validScore,
    skills_matched: matchedSkills,
    skills_missing: missingSkills,
    message: `Found ${matchedSkills.length} matching skills out of ${effectiveJobSkills.length} required skills`
  };
};

/**
 * Calculate string similarity between two strings (for fuzzy skill matching)
 * Returns a value between 0 and 1, where 1 means perfect match
 */
function calculateStringSimilarity(str1, str2) {
  // Direct match
  if (str1 === str2) return 1.0;

  // One string contains the other
  if (str1.includes(str2)) return 0.9;
  if (str2.includes(str1)) return 0.9;

  // Calculate Levenshtein distance (basic implementation)
  const len1 = str1.length;
  const len2 = str2.length;

  // If either string is empty, similarity is 0
  if (len1 === 0 || len2 === 0) return 0;

  // If strings are short, use a simpler comparison
  if (len1 < 3 || len2 < 3) {
    return str1[0] === str2[0] ? 0.7 : 0;
  }

  // Check if strings share common terms
  const words1 = str1.split(/\s+/);
  const words2 = str2.split(/\s+/);

  let commonWords = 0;
  words1.forEach(w1 => {
    if (words2.some(w2 => w1 === w2 || w1.includes(w2) || w2.includes(w1))) {
      commonWords++;
    }
  });

  if (commonWords > 0) {
    return commonWords / Math.max(words1.length, words2.length);
  }

  // For longer strings, look for common prefix/suffix
  const prefixLength = commonPrefixLength(str1, str2);
  const suffixLength = commonSuffixLength(str1, str2);

  // If there's a significant common prefix or suffix, consider it similar
  if (prefixLength >= 3 || suffixLength >= 3) {
    return (prefixLength + suffixLength) / (len1 + len2);
  }

  // Default to a lower similarity
  return 0.1;
}

/**
 * Find length of common prefix between two strings
 */
function commonPrefixLength(str1, str2) {
  const minLength = Math.min(str1.length, str2.length);
  let i = 0;
  while (i < minLength && str1[i] === str2[i]) {
    i++;
  }
  return i;
}

/**
 * Find length of common suffix between two strings
 */
function commonSuffixLength(str1, str2) {
  const minLength = Math.min(str1.length, str2.length);
  let i = 0;
  while (i < minLength &&
         str1[str1.length - 1 - i] === str2[str2.length - 1 - i]) {
    i++;
  }
  return i;
}

/**
 * Extract skills from a profile or job object
 */
function extractSkills(obj) {
  if (!obj) return [];

  const skills = [];
  console.log('Extracting skills from:', obj);

  // If skills array is available directly, use it
  if (obj.skills && Array.isArray(obj.skills)) {
    skills.push(...obj.skills.map(skill =>
      typeof skill === 'string' ? skill : (skill.name || '')
    ).filter(Boolean));
  }

  // Check for skills in data object
  if (obj.data) {
    // Direct skills array in data
    if (obj.data.skills && Array.isArray(obj.data.skills)) {
      skills.push(...obj.data.skills.map(skill =>
        typeof skill === 'string' ? skill : (skill.name || '')
      ).filter(Boolean));
    }

    // Technologies in repositories
    if (obj.data.repositories && Array.isArray(obj.data.repositories)) {
      obj.data.repositories.forEach(repo => {
        if (repo.languages && Array.isArray(repo.languages)) {
          skills.push(...repo.languages);
        }
        if (repo.technologies && Array.isArray(repo.technologies)) {
          skills.push(...repo.technologies);
        }
        if (repo.language) {
          skills.push(repo.language);
        }
        // Look at repository name and description for tech keywords
        if (repo.name) {
          const repoNameKeywords = extractTechKeywords(repo.name);
          skills.push(...repoNameKeywords);
        }
        if (repo.description) {
          const repoDescKeywords = extractTechKeywords(repo.description);
          skills.push(...repoDescKeywords);
        }
      });
    }

    // Check for profile information that might contain skills
    if (obj.data.bio) {
      const techKeywords = extractTechKeywords(obj.data.bio);
      skills.push(...techKeywords);
    }
  }

  // For LinkedIn profiles, check for additional skill locations
  if (obj.platform === 'linkedin' || (obj.username && obj.username.includes('linkedin.com'))) {
    // Sometimes stored in experience descriptions
    if (obj.data && obj.data.experience && Array.isArray(obj.data.experience)) {
      obj.data.experience.forEach(exp => {
        if (exp.description) {
          const techKeywords = extractTechKeywords(exp.description);
          skills.push(...techKeywords);
        }
        if (exp.title) {
          const titleKeywords = extractTechKeywords(exp.title);
          skills.push(...titleKeywords);
        }
      });
    }

    // Extract from the URL if it's a LinkedIn profile
    if (obj.username && obj.username.includes('linkedin.com')) {
      // Add default LinkedIn skills since we can't scrape them directly
      skills.push('LinkedIn', 'Networking', 'Professional', 'Communication');

      // Extract any identifiable keywords from the URL
      const parts = obj.username.split('/');
      const lastPart = parts[parts.length - 1];
      if (lastPart && lastPart !== '' && !lastPart.includes('linkedin.com')) {
        const urlKeywords = extractTechKeywords(lastPart.replace(/-/g, ' '));
        skills.push(...urlKeywords);
      }
    }
  }

  // For GitHub profiles, extract from repos and languages
  if (obj.platform === 'github' || (obj.username && !obj.username.includes('linkedin.com'))) {
    // If it's a GitHub username, infer some basic skills
    if (obj.username && !obj.username.includes('http')) {
      skills.push('GitHub', 'Git', 'Version Control');

      // Add common programming skills as we don't have detailed data
      skills.push('Programming', 'Software Development', 'Coding');
    }

    if (obj.data && obj.data.repositories) {
      obj.data.repositories.forEach(repo => {
        if (repo.language) skills.push(repo.language);
        if (repo.languages) skills.push(...repo.languages);
      });
    }
  }

  // Check job title and description for tech keywords
  if (obj.title) {
    const titleKeywords = extractTechKeywords(obj.title);
    skills.push(...titleKeywords);
  }

  if (obj.description) {
    const descKeywords = extractTechKeywords(obj.description);
    skills.push(...descKeywords);
  }

  // Check bio for tech keywords
  if (obj.bio) {
    const techKeywords = extractTechKeywords(obj.bio);
    skills.push(...techKeywords);
  }

  // Handle case where no skills were found but we have a username
  if (skills.length === 0 && obj.username) {
    // Try to extract anything useful from the username
    const usernameKeywords = extractTechKeywords(obj.username);
    if (usernameKeywords.length > 0) {
      skills.push(...usernameKeywords);
    }

    // If still no skills, add generic skills based on platform
    if (skills.length === 0) {
      if (obj.platform === 'github' || (obj.username && !obj.username.includes('linkedin.com'))) {
        skills.push('GitHub', 'Programming', 'Software Development', 'Coding');
      } else if (obj.platform === 'linkedin' || (obj.username && obj.username.includes('linkedin.com'))) {
        skills.push('LinkedIn', 'Professional Networking', 'Communication', 'Professional Skills');
      }
    }
  }

  // If still no skills found and this is a job, extract from company name
  if (skills.length === 0 && obj.company) {
    const companyKeywords = extractTechKeywords(obj.company);
    skills.push(...companyKeywords);

    // Add generic job skills
    skills.push('Professional', 'Communication', 'Teamwork');
  }

  // Clean and deduplicate skills
  return [...new Set(skills.map(s => s?.trim()).filter(Boolean))];
}

/**
 * Extract technical keywords from text
 */
function extractTechKeywords(text) {
  if (!text) return [];

  // List of common tech keywords to search for
  const techKeywords = [
    "JavaScript", "JS", "TypeScript", "TS", "React", "Angular", "Vue", "Node", "Express",
    "MongoDB", "SQL", "PostgreSQL", "MySQL", "Firebase", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "CI/CD", "Git", "GitHub", "GitLab", "Python", "Django", "Flask",
    "Java", "Spring", "C#", ".NET", "C++", "Ruby", "Rails", "PHP", "Laravel", "Symfony",
    "HTML", "CSS", "SASS", "SCSS", "Bootstrap", "Tailwind", "Redux", "GraphQL", "REST API",
    "Agile", "Scrum", "TDD", "Jest", "Mocha", "Cypress", "WebPack", "Babel", "ESLint",
    "Responsive Design", "Mobile Development", "Android", "iOS", "Swift", "Kotlin",
    "Machine Learning", "AI", "Data Science", "Big Data", "Hadoop", "Spark", "TensorFlow",
    "Blockchain", "Ethereum", "Solidity", "DevOps", "Linux", "Unix", "Bash", "Shell",
    "PowerShell", "Frontend", "Backend", "Fullstack", "Web Development", "Software Engineering",
    "Algorithm", "Data Structure", "Database", "Networking", "Security", "Cloud Computing",
    "Microservices", "API Design", "UI/UX", "Testing", "QA", "Debugging", "Performance Optimization",
    "Go", "Golang", "Rust", "Scala", "Clojure", "Haskell", "Erlang", "Elixir", "F#", "OCaml",
    "R", "Julia", "MATLAB", "Perl", "Assembly", "COBOL", "Fortran", "Lisp", "Scheme",
    "Next.js", "Gatsby", "Svelte", "jQuery", "Ember", "Backbone", "Knockout", "D3.js",
    "Three.js", "WebGL", "Canvas", "SVG", "Web Components", "PWA", "Service Workers",
    "WebSockets", "WebRTC", "WebAssembly", "WASM",
    "Senior", "Junior", "Developer", "Engineer", "Architect", "Lead", "Manager", "Director",
    "Programmer", "SDE", "SWE"
  ];

  const textLower = text.toLowerCase();

  // Find all tech keywords in the text
  const found = techKeywords.filter(keyword =>
    textLower.includes(keyword.toLowerCase())
  );

  // Also try to extract words that look like programming terms or technologies
  const words = textLower.split(/[\s\-_.,;:!?()[\]{}|\\/"']+/);
  const potentialTechWords = words.filter(word => {
    // Words that look like tech terms often have mixed case (camelCase, PascalCase)
    // or contain special characters common in tech (.js, .py, etc)
    return (word.length > 1 && /^[a-z]+[A-Z][a-z]*/.test(word)) || // camelCase
           (word.length > 1 && /^[A-Z][a-z]+[A-Z]/.test(word)) ||  // PascalCase
           /\.[a-z]{1,4}$/.test(word) ||  // file extensions (.js, .py, etc)
           /^[a-z]+\-[a-z]+$/.test(word); // hyphenated tech terms
  });

  return [...new Set([...found, ...potentialTechWords])];
}

/**
 * Check if two skills are similar
 */
function isSimilarSkill(skill1, skill2) {
  if (!skill1 || !skill2) return false;

  const s1 = skill1.toLowerCase();
  const s2 = skill2.toLowerCase();

  return s1 === s2 || s1.includes(s2) || s2.includes(s1);
}

export default {
  calculateMatch,
  calculateCombinedMatch,
  combineProfiles,
  performLocalMatch
};