import api from './api';

/**
 * Get all GitHub profiles
 * @returns {Promise<Array>} Array of GitHub profiles
 */
export const getAllProfiles = async () => {
  try {
    // Use localStorage fallback when the API is unavailable
    try {
      const response = await api.get('/profile/github');
      return response.data || [];
    } catch (error) {
      console.warn('Falling back to local storage for profiles');
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      return profiles;
    }
  } catch (error) {
    console.error('Error fetching profiles:', error);
    return [];
  }
};

/**
 * Get a specific GitHub profile
 * @param {string} username - GitHub username
 * @returns {Promise<Object>} GitHub profile data
 */
export const getProfile = async (username) => {
  try {
    // Using the correct Flask endpoint pattern: /profile/{platform}/{username}
    const response = await api.get(`/profile/github/${username}`);

    // Store in localStorage for offline access
    if (response && response.profile) {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const existingIndex = profiles.findIndex(p => p.username === username);

      if (existingIndex >= 0) {
        profiles[existingIndex] = response.profile;
      } else {
        profiles.push(response.profile);
      }

      localStorage.setItem('profiles', JSON.stringify(profiles));
    }

    return response;
  } catch (error) {
    console.error(`Error fetching profile for ${username}:`, error);

    // Try to get from localStorage as fallback
    try {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const profile = profiles.find(p => p.username === username);
      if (profile) {
        console.log('Using cached profile from localStorage');
        return { profile, status: 'success' };
      }
    } catch (e) {
      console.error('Error reading from localStorage:', e);
    }

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
    // Use the validated API endpoint
    const response = await api.get(`/profile/github/${username}`);
    // Cache the profile in localStorage
    if (response && response.profile) {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const existingIndex = profiles.findIndex(p =>
        p.username === username && p.platform === 'github'
      );

      if (existingIndex >= 0) {
        profiles[existingIndex] = {
          ...response.profile,
          platform: 'github'
        };
      } else {
        profiles.push({
          ...response.profile,
          platform: 'github'
        });
      }

      localStorage.setItem('profiles', JSON.stringify(profiles));
    }

    return response.profile;
  } catch (error) {
    console.error(`Error fetching profile for ${username}:`, error);

    // Check if profile exists in localStorage
    try {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const cachedProfile = profiles.find(p =>
        p.username === username && p.platform === 'github'
      );

      if (cachedProfile) {
        console.log('Using cached GitHub profile from localStorage');
        return cachedProfile;
      }
    } catch (e) {
      console.error('Error reading from localStorage:', e);
    }

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
    // First try to delete from the API
    try {
      const response = await api.delete(`/profile/github/${username}`);
      return response;
    } catch (apiError) {
      // If API fails, just remove from localStorage
      console.warn('API unavailable, removing from localStorage only');
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const filteredProfiles = profiles.filter(p => p.username !== username);
      localStorage.setItem('profiles', JSON.stringify(filteredProfiles));
      return { status: 'success', message: 'Profile removed from local storage' };
    }
  } catch (error) {
    console.error(`Error deleting profile for ${username}:`, error);
    throw error;
  }
};