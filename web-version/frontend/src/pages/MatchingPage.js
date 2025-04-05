import React, { useState, useEffect, useCallback } from 'react';
import MatchForm from '../components/MatchForm';
import { calculateMatch, calculateCombinedMatch, performLocalMatch } from '../services/matchService';
import CombinedProfileSelector from '../components/CombinedProfileSelector';

const MatchingPage = () => {
  const [profiles, setProfiles] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [useCombinedMode, setUseCombinedMode] = useState(false);
  const [selectedCombinedProfiles, setSelectedCombinedProfiles] = useState([]);

  // Use useCallback to memoize the loadDataFromStorage function
  const loadDataFromStorage = useCallback(() => {
    try {
      setLoading(true);
      setErrorMessage(null);

      // Load profiles
      const savedProfiles = localStorage.getItem('profiles');
      if (savedProfiles) {
        const parsedProfiles = JSON.parse(savedProfiles);
        console.log('Loaded profiles from storage:', parsedProfiles);
        setProfiles(parsedProfiles);
      }

      // Load jobs
      const savedJobs = localStorage.getItem('jobs');
      if (savedJobs) {
        const parsedJobs = JSON.parse(savedJobs);
        console.log('Loaded jobs from storage:', parsedJobs);
        setJobs(parsedJobs);
      }

      // Load matches and handle legacy data
      const savedMatches = localStorage.getItem('matches');
      if (savedMatches) {
        const parsedMatches = JSON.parse(savedMatches);
        console.log('Loaded matches from storage:', parsedMatches);
        setMatches(upgradeLegacyMatches(parsedMatches));
      }

      setLoading(false);
    } catch (err) {
      setErrorMessage('Failed to load data from storage');
      console.error('Error loading data from storage:', err);
      setLoading(false);
    }
  }, []);

  // Load existing data on component mount
  useEffect(() => {
    loadDataFromStorage();
  }, [loadDataFromStorage]);

  // Save matches to localStorage whenever they change
  useEffect(() => {
    if (matches && matches.length > 0) {
      localStorage.setItem('matches', JSON.stringify(matches));
    }
  }, [matches]);

  // Handle legacy match data that might not have skill information
  const upgradeLegacyMatches = (matchesData) => {
    if (!matchesData || !Array.isArray(matchesData)) return [];

    return matchesData.map(match => {
      if (!match) return null;

      // Make sure we have a consistent naming convention
      const newMatch = { ...match };

      // Convert old matchedSkills to skills_matched if present
      if (match.matchedSkills && !match.skills_matched) {
        newMatch.skills_matched = match.matchedSkills;
        delete newMatch.matchedSkills;
      } else if (!match.skills_matched) {
        newMatch.skills_matched = [];
      }

      // Convert old missingSkills to skills_missing if present
      if (match.missingSkills && !match.skills_missing) {
        newMatch.skills_missing = match.missingSkills;
        delete newMatch.missingSkills;
      } else if (!match.skills_missing) {
        newMatch.skills_missing = [];
      }

      return newMatch;
    }).filter(Boolean);
  };

  // Handle when user toggles between single and combined profile mode
  const handleToggleCombinedMode = () => {
    setUseCombinedMode(!useCombinedMode);
    // Reset selected profiles when toggling off combined mode
    if (useCombinedMode) {
      setSelectedCombinedProfiles([]);
    }
  };

  // Handle match submission with support for combined profiles
  const handleMatchSubmit = async (formData) => {
    try {
      setLoading(true);
      setErrorMessage(null);

      // Get job details
      console.log('Starting match calculation for job:', formData.job);
      const job = jobs.find(j => j.id === formData.job) || null;

      if (!job) {
        setErrorMessage('Job not found');
        setLoading(false);
        return;
      }

      let matchResult;

      if (useCombinedMode && selectedCombinedProfiles.length > 0) {
        console.log('Using combined profiles for matching:', selectedCombinedProfiles);

        if (selectedCombinedProfiles.length === 0) {
          setErrorMessage('Please select at least one profile');
          setLoading(false);
          return;
        }

        try {
          matchResult = await calculateCombinedMatch(selectedCombinedProfiles, job);
          console.log('API combined match result:', matchResult);
        } catch (e) {
          console.error('Error using API for combined match, falling back to local:', e);
          // If API fails, try to calculate for each profile individually and take average
          matchResult = await calculateCombinedMatch(selectedCombinedProfiles, job);
        }
      } else {
        // Single profile matching
        const profileId = formData.profile;
        console.log('Using single profile for matching:', profileId);

        if (!profileId) {
          setErrorMessage('Please select a profile');
          setLoading(false);
          return;
        }

        const profile = profiles.find(p => p.id === profileId || p.username === profileId);

        if (!profile) {
          setErrorMessage('Profile not found');
          setLoading(false);
          return;
        }

        try {
          matchResult = await calculateMatch(profile, job);
          console.log('API match result:', matchResult);
        } catch (e) {
          console.error('Error using API for match, falling back to local:', e);
          matchResult = await calculateMatch(profile, job);
        }
      }

      // Create new match object
      const matchId = `match-${Date.now()}`;
      const timestamp = new Date().toISOString();

      const newMatch = {
        id: matchId,
        profileId: useCombinedMode ? selectedCombinedProfiles.map(p => p.username || p.id).join(',') : formData.profile,
        jobId: formData.job,
        score: matchResult.overall_score || 0.5,
        timestamp,
        skills_matched: matchResult.skills_matched || [],
        skills_missing: matchResult.skills_missing || [],
        platforms: useCombinedMode ? matchResult.platforms : [profiles.find(p => p.id === formData.profile)?.platform],
        usedCombinedProfiles: useCombinedMode
      };

      console.log(`New ${useCombinedMode ? 'combined' : 'single'} match saved:`, newMatch);

      // Add to matches
      const updatedMatches = [...matches, newMatch];
      setMatches(updatedMatches);

      // Save to localStorage
      localStorage.setItem('matches', JSON.stringify(updatedMatches));

      setLoading(false);
    } catch (err) {
      setErrorMessage('Failed to calculate match: ' + (err.message || 'Unknown error'));
      setLoading(false);
      console.error('Error in match calculation:', err);
    }
  };

  const handleDeleteMatch = (matchId) => {
    try {
      setLoading(true);
      console.log('Deleting match with ID:', matchId);
      const updatedMatches = matches.filter(match => match.id !== matchId);
      setMatches(updatedMatches);
      localStorage.setItem('matches', JSON.stringify(updatedMatches));
      setLoading(false);
    } catch (err) {
      setErrorMessage('Failed to delete match');
      setLoading(false);
      console.error('Error deleting match:', err);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Profile Matching</h1>

      {errorMessage && (
        <div className="mb-4 p-3 bg-red-100 border-l-4 border-red-500 text-red-700">
          <p>{errorMessage}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">Create New Match</h2>

              <div className="flex items-center">
                <span className="mr-2 text-sm text-gray-600">
                  {useCombinedMode ? 'Combined Mode' : 'Single Profile'}
                </span>
                <button
                  onClick={handleToggleCombinedMode}
                  className="relative inline-flex items-center h-6 rounded-full w-11 bg-gray-200 focus:outline-none"
                >
                  <span
                    className={`inline-block w-4 h-4 transform transition-transform ${
                      useCombinedMode ? 'translate-x-6 bg-blue-600' : 'translate-x-1 bg-white'
                    } rounded-full shadow-lg`}
                  />
                </button>
              </div>
            </div>

            {useCombinedMode && (
              <div className="mb-4">
                <CombinedProfileSelector
                  profiles={profiles}
                  selectedProfiles={selectedCombinedProfiles}
                  onSelectProfiles={setSelectedCombinedProfiles}
                />
              </div>
            )}

            <MatchForm
              profiles={profiles}
              jobs={jobs}
              onSubmit={handleMatchSubmit}
              isLoading={loading}
              useCombinedMode={useCombinedMode}
              selectedProfileCount={selectedCombinedProfiles.length}
            />
          </div>

          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Match Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {matches.map(match => {
                const job = jobs.find(j => j.id === match.jobId);
                const profileInfo = match.usedCombinedProfiles
                  ? `Combined profiles (${match.platforms?.join(', ')})`
                  : profiles.find(p => p.id === match.profileId || p.username === match.profileId)?.name || match.profileId;

                return (
                  <div key={match.id} className="border rounded-lg shadow-md p-4 bg-white relative">
                    <button
                      onClick={() => handleDeleteMatch(match.id)}
                      className="absolute top-2 right-2 text-red-500 hover:text-red-700"
                      title="Delete match"
                    >
                      ×
                    </button>

                    <h3 className="font-bold text-lg">{profileInfo} → {job?.title} at {job?.company}</h3>
                    <p className="text-sm text-gray-600">
                      Platform: {match.platforms?.join(', ') || 'Unknown'} • {new Date(match.timestamp).toLocaleString()}
                    </p>
                    <div className="mt-4">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="font-bold text-xl">{Math.round(match.score * 100)}%</div>
                        <div>Match Score</div>
                      </div>

                      <div className="mt-4">
                        <h4 className="font-bold">Matching Skills:</h4>
                        {match.skills_matched && match.skills_matched.length > 0 ? (
                          <div className="flex flex-wrap gap-1 mt-1">
                            {match.skills_matched.map((skill, i) => (
                              <span key={i} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                                {skill}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">No matching skills found</p>
                        )}
                      </div>

                      <div className="mt-2">
                        <h4 className="font-bold">Missing Skills:</h4>
                        {match.skills_missing && match.skills_missing.length > 0 ? (
                          <div className="flex flex-wrap gap-1 mt-1">
                            {match.skills_missing.map((skill, i) => (
                              <span key={i} className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                                {skill}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500">No missing skills found</p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div>
          <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-2xl font-bold mb-4">Profiles</h2>
            {profiles.length === 0 ? (
              <p className="text-gray-600">No profiles yet. Create profiles in their respective sections.</p>
            ) : (
              <div className="space-y-4">
                {profiles.map((profile, index) => {
                  if (!profile) return null;
                  const profileId = profile.id || profile.username || `unknown-${index}`;
                  const displayName = profile.name || profile.username || `Profile ${index + 1}`;

                  // Extract skills
                  const profileSkills = [];
                  if (profile.skills && Array.isArray(profile.skills)) {
                    profile.skills.forEach(skill => {
                      if (typeof skill === 'string') {
                        profileSkills.push(skill);
                      } else if (skill && typeof skill === 'object' && skill.name) {
                        profileSkills.push(skill.name);
                      }
                    });
                  }

                  return (
                    <div key={profileId} className="p-3 border rounded">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <div className="font-medium">{displayName}</div>
                          <div className="text-xs text-gray-500">
                            {profile.platform && <span className="mr-1">{profile.platform}</span>}
                            {profile.username && <span className="mr-1">@{profile.username}</span>}
                          </div>
                        </div>
                      </div>

                      {/* Skills */}
                      <div className="mt-2">
                        <h4 className="text-xs font-medium text-gray-700 mb-1">Skills:</h4>
                        <div className="flex flex-wrap gap-1">
                          {profileSkills.length > 0 ? (
                            profileSkills.map((skill, idx) => (
                              <span
                                key={idx}
                                className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                              >
                                {skill}
                              </span>
                            ))
                          ) : (
                            <span className="text-xs text-gray-500">No skills found</span>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">Jobs</h2>
            {jobs.length === 0 ? (
              <p className="text-gray-600">No jobs yet. Create jobs in the Jobs section.</p>
            ) : (
              <div className="space-y-4">
                {jobs.map((job, index) => {
                  if (!job) return null;
                  const jobId = job.id || `unknown-${index}`;

                  // Extract job skills
                  const jobSkills = [];
                  if (job.skills && Array.isArray(job.skills)) {
                    job.skills.forEach(skill => {
                      if (typeof skill === 'string') {
                        jobSkills.push(skill);
                      } else if (skill && typeof skill === 'object' && skill.name) {
                        jobSkills.push(skill.name);
                      }
                    });
                  }

                  return (
                    <div key={jobId} className="p-3 border rounded">
                      <div className="mb-2">
                        <div className="font-medium">{job.title || `Job ${index + 1}`}</div>
                        <div className="text-xs text-gray-500">
                          {job.company && <span>{job.company}</span>}
                        </div>
                      </div>

                      {/* Skills */}
                      <div className="mt-2">
                        <h4 className="text-xs font-medium text-gray-700 mb-1">Required Skills:</h4>
                        <div className="flex flex-wrap gap-1">
                          {jobSkills.length > 0 ? (
                            jobSkills.map((skill, idx) => (
                              <span
                                key={idx}
                                className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                              >
                                {skill}
                              </span>
                            ))
                          ) : (
                            <span className="text-xs text-gray-500">No skills specified</span>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchingPage;