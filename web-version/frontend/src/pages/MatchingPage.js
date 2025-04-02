import React, { useState, useEffect } from 'react';
import MatchForm from '../components/MatchForm';
import MatchResultCard from '../components/MatchResultCard';
import { matchProfileToJob } from '../services/matchService';

const MatchingPage = () => {
  const [profiles, setProfiles] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [matchStatus, setMatchStatus] = useState({ loading: false, error: null });

  // Load existing data on component mount
  useEffect(() => {
    loadDataFromStorage();
  }, []);

  // Save matches to localStorage whenever they change
  useEffect(() => {
    if (matches && matches.length > 0) {
      localStorage.setItem('matches', JSON.stringify(matches));
    }
  }, [matches]);

  const loadDataFromStorage = () => {
    try {
      setLoading(true);
      setError(null);

      // Load profiles
      const savedProfiles = localStorage.getItem('profiles');
      if (savedProfiles) {
        setProfiles(JSON.parse(savedProfiles));
      }

      // Load jobs
      const savedJobs = localStorage.getItem('jobs');
      if (savedJobs) {
        setJobs(JSON.parse(savedJobs));
      }

      // Load matches
      const savedMatches = localStorage.getItem('matches');
      if (savedMatches) {
        setMatches(JSON.parse(savedMatches));
      }

      setLoading(false);
    } catch (err) {
      setError('Failed to load data from storage');
      console.error('Error loading data from storage:', err);
      setLoading(false);
    }
  };

  const handleMatchSubmit = async ({ profileId, jobId }) => {
    if (!profileId || !jobId) {
      setMatchStatus({
        loading: false,
        error: 'Profile or job ID is missing'
      });
      return;
    }

    try {
      setMatchStatus({ loading: true, error: null });

      // Find the profile and job objects
      const profile = profiles.find(p => p?.username === profileId || p?.id === profileId);
      const job = jobs.find(j => j?.id === jobId);

      if (!profile || !job) {
        throw new Error('Profile or job not found');
      }

      let matchResult;

      // Try to use the API first
      try {
        matchResult = await matchProfileToJob(profileId, jobId);
      } catch (apiError) {
        console.error('API error, calculating match locally:', apiError);

        // Fall back to a simple local match calculation
        matchResult = calculateLocalMatch(profile, job);
      }

      // Add to matches list (or replace if exists)
      setMatches(prevMatches => {
        // See if we already have a match for this profile and job
        const existingIndex = prevMatches.findIndex(
          m => (m.profile_id === profileId || m.profile_name === profile.name) && m.job_id === jobId
        );

        if (existingIndex >= 0) {
          const updatedMatches = [...prevMatches];
          updatedMatches[existingIndex] = matchResult;
          return updatedMatches;
        } else {
          return [...prevMatches, matchResult];
        }
      });

      setMatchStatus({ loading: false, error: null });
    } catch (err) {
      setMatchStatus({
        loading: false,
        error: err.displayMessage || err.message || 'Failed to calculate match'
      });
      console.error('Error calculating match:', err);
    }
  };

  const handleDeleteMatch = async (matchId) => {
    if (!matchId) return;

    if (window.confirm('Are you sure you want to delete this match result?')) {
      try {
        setLoading(true);

        // Remove from matches list in state
        setMatches(prevMatches => prevMatches.filter(match => match?.id !== matchId));

        // Also remove from localStorage
        const savedMatches = JSON.parse(localStorage.getItem('matches') || '[]');
        const updatedMatches = savedMatches.filter(match => match?.id !== matchId);
        localStorage.setItem('matches', JSON.stringify(updatedMatches));

        setLoading(false);
      } catch (err) {
        setError(err.displayMessage || 'Failed to delete match');
        setLoading(false);
        console.error('Error deleting match:', err);
      }
    }
  };

  // Simple local matching algorithm
  const calculateLocalMatch = (profile, job) => {
    const profileSkills = extractProfileSkills(profile);
    const jobSkills = extractJobSkills(job);

    // Calculate matches
    let totalImportance = 0;
    let matchedImportance = 0;
    const skillMatches = [];
    const missingSkills = [];

    jobSkills.forEach(jobSkill => {
      const jobSkillName = jobSkill.name.toLowerCase();
      const importance = jobSkill.importance || 0.5;
      totalImportance += importance;

      // Find matching profile skill
      const matchingSkill = profileSkills.find(s =>
        s.name.toLowerCase() === jobSkillName ||
        s.name.toLowerCase().includes(jobSkillName) ||
        jobSkillName.includes(s.name.toLowerCase())
      );

      if (matchingSkill) {
        // Get proficiency level from skill object or default to 1.0
        const proficiency = matchingSkill.proficiency || 1.0;

        // Calculate match quality based on skill name match type
        let matchQuality = 0.7; // Default for partial matches

        // Exact match gets higher quality score
        if (matchingSkill.name.toLowerCase() === jobSkillName) {
          matchQuality = 1.0;
        }

        // Final match score combines match quality and proficiency
        const matchScore = matchQuality * proficiency;

        // Add to matched importance with weighting
        matchedImportance += importance * matchScore;

        skillMatches.push({
          skill_name: jobSkill.name,
          importance: importance,
          proficiency: proficiency,
          match_quality: matchQuality,
          match_score: matchScore,
          weighted_score: importance * matchScore,
          required: jobSkill.required || false
        });
      } else {
        missingSkills.push({
          name: jobSkill.name,
          importance: importance,
          required: jobSkill.required || false
        });
      }
    });

    // Calculate overall match percentage
    const overallMatch = Math.round((matchedImportance / totalImportance) * 100);

    // Generate recommendation
    let recommendation = '';
    if (overallMatch >= 85) {
      recommendation = 'Excellent Match: This candidate has most of the required skills and would be an excellent fit for this position.';
    } else if (overallMatch >= 70) {
      recommendation = 'Good Match: This candidate has many of the required skills and would likely be a good fit with some training.';
    } else if (overallMatch >= 50) {
      recommendation = 'Moderate Match: This candidate has some of the required skills but may need significant training or may not be ideal for this specific role.';
    } else if (overallMatch >= 30) {
      recommendation = 'Weak Match: This candidate is missing many critical skills required for this position.';
    } else {
      recommendation = 'Poor Match: This candidate does not appear to have the necessary skills for this position.';
    }

    // Check if any required skills are missing
    const missingRequiredSkills = missingSkills.filter(skill => skill.required);
    if (missingRequiredSkills.length > 0) {
      recommendation += ` Missing ${missingRequiredSkills.length} required skill(s).`;
    }

    // Find strengths (high-matching important skills)
    const strengths = skillMatches
      .filter(match => match.importance >= 0.7 && match.match_score >= 0.7)
      .map(match => match.skill_name);

    return {
      id: `match_${Date.now()}`,
      profile_id: profile.id || profile.username,
      profile_name: profile.name || profile.username,
      job_id: job.id,
      job_title: job.title,
      company: job.company,
      overall_match: overallMatch,
      skill_matches: skillMatches,
      missing_skills: missingSkills.map(s => s.name), // Keep backward compatibility
      missing_skills_details: missingSkills, // Include full details
      strengths: strengths,
      recommendation: recommendation,
      created_at: new Date().toISOString()
    };
  };

  // Extract skills from profile in a consistent format
  const extractProfileSkills = (profile) => {
    if (!profile) return [];

    const skills = [];

    if (profile.skills && Array.isArray(profile.skills)) {
      profile.skills.forEach(skill => {
        if (typeof skill === 'string') {
          skills.push({ name: skill });
        } else if (skill && skill.name) {
          skills.push({
            name: skill.name,
            proficiency: skill.proficiency || skill.level || 1.0
          });
        }
      });
    }

    return skills;
  };

  // Extract skills from job in a consistent format
  const extractJobSkills = (job) => {
    if (!job) return [];

    const skills = [];

    if (job.skills && Array.isArray(job.skills)) {
      job.skills.forEach(skill => {
        if (typeof skill === 'string') {
          skills.push({ name: skill, importance: 0.5 });
        } else if (skill && skill.name) {
          skills.push({
            name: skill.name,
            importance: skill.importance || 0.5
          });
        }
      });
    }

    return skills;
  };

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">Profile-Job Matching</h1>

      {/* Error display */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 border-l-4 border-red-500 text-red-700">
          <p>{error}</p>
        </div>
      )}

      {/* Match form */}
      <div className="mb-8">
        <MatchForm
          profiles={profiles}
          jobs={jobs}
          onSubmit={handleMatchSubmit}
          isLoading={matchStatus.loading}
        />

        {matchStatus.error && (
          <div className="mt-4 p-3 bg-red-100 border-l-4 border-red-500 text-red-700">
            <p>{matchStatus.error}</p>
          </div>
        )}
      </div>

      {/* Match results listing */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Match Results</h2>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : matches.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 text-center">
            <p className="text-gray-500">
              No match results yet. Create one using the form above.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {matches.map((match) => (
              <div key={match.id || `${match.profile_id}-${match.job_id}`} className="relative">
                <MatchResultCard matchResult={match} />
                <button
                  onClick={() => handleDeleteMatch(match.id)}
                  className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1"
                  aria-label="Delete match"
                  title="Delete match"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchingPage;