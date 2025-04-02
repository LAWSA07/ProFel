import api from './api';

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