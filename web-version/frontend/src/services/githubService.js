import api from './api';

/**
 * Get all GitHub profiles
 * @returns {Promise<Array>} Array of GitHub profiles
 */
export const getAllProfiles = async () => {
  try {
    // This endpoint should be implemented on the backend
    const response = await api.get('/github/profiles');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching profiles:', error);
    throw error;
  }
};

/**
 * Get a specific GitHub profile
 * @param {string} username - GitHub username
 * @returns {Promise<Object>} GitHub profile data
 */
export const getProfile = async (username) => {
  try {
    // Using the profile endpoint
    const response = await api.post('/github/profile', { username });
    return response.data;
  } catch (error) {
    console.error(`Error fetching profile for ${username}:`, error);
    throw error;
  }
};

/**
 * Fetch and process a GitHub profile
 * @param {string} username - GitHub username
 * @returns {Promise<Object>} Processed GitHub profile data
 */
export const fetchProfile = async (username) => {
  try {
    // Same as getProfile since the backend processes the profile
    const response = await api.post('/github/profile', { username });
    return response.data;
  } catch (error) {
    console.error(`Error fetching profile for ${username}:`, error);
    throw error;
  }
};

/**
 * Delete a GitHub profile
 * @param {string} username - GitHub username
 * @returns {Promise<Object>} Response data
 */
export const deleteProfile = async (username) => {
  try {
    // This endpoint should be implemented on the backend
    const response = await api.delete(`/github/profiles/${username}`);
    return response;
  } catch (error) {
    console.error(`Error deleting profile for ${username}:`, error);
    throw error;
  }
};