import api from './api';

/**
 * Get all profiles from a specific platform
 * @param {string} platform - Platform name (github, linkedin, leetcode)
 * @returns {Promise<Array>} Array of profiles
 */
export const getAllProfiles = async (platform) => {
  try {
    // Try to get from API first
    try {
      const response = await api.get(`/profile/${platform}`);
      return response.data || [];
    } catch (error) {
      console.warn(`Falling back to local storage for ${platform} profiles`);
      // Filter profiles from localStorage by platform
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      return profiles.filter(p => p.platform === platform);
    }
  } catch (error) {
    console.error(`Error fetching ${platform} profiles:`, error);
    return [];
  }
};

/**
 * Get a specific profile by username and platform
 * @param {string} platform - Platform name (github, linkedin, leetcode)
 * @param {string} username - Username on the platform
 * @returns {Promise<Object>} Profile data
 */
export const getProfile = async (platform, username) => {
  try {
    // Using the correct endpoint pattern: /profile/{platform}/{username}
    const response = await api.get(`/profile/${platform}/${username}`);

    // Store in localStorage for offline access
    if (response && response.profile) {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const existingIndex = profiles.findIndex(p =>
        p.username === username && p.platform === platform
      );

      if (existingIndex >= 0) {
        profiles[existingIndex] = {
          ...response.profile,
          platform
        };
      } else {
        profiles.push({
          ...response.profile,
          platform
        });
      }

      localStorage.setItem('profiles', JSON.stringify(profiles));
    }

    return response.profile;
  } catch (error) {
    console.error(`Error fetching ${platform} profile for ${username}:`, error);

    // Try to get from localStorage as fallback
    try {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const profile = profiles.find(p =>
        p.username === username && p.platform === platform
      );

      if (profile) {
        console.log(`Using cached ${platform} profile from localStorage`);
        return profile;
      }
    } catch (e) {
      console.error('Error reading from localStorage:', e);
    }

    throw error;
  }
};

/**
 * Fetch and process a profile from any supported platform
 * @param {string} platform - Platform name (github, linkedin, leetcode)
 * @param {string} username - Username on the platform
 * @returns {Promise<Object>} Processed profile data
 */
export const fetchProfile = async (platform, username) => {
  try {
    // Use the API endpoint for the specific platform
    const response = await api.get(`/profile/${platform}/${username}`);

    // Cache the profile in localStorage
    if (response && response.profile) {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const existingIndex = profiles.findIndex(p =>
        p.username === username && p.platform === platform
      );

      if (existingIndex >= 0) {
        profiles[existingIndex] = {
          ...response.profile,
          platform
        };
      } else {
        profiles.push({
          ...response.profile,
          platform
        });
      }

      localStorage.setItem('profiles', JSON.stringify(profiles));
    }

    return response.profile;
  } catch (error) {
    console.error(`Error fetching ${platform} profile for ${username}:`, error);

    // Check if profile exists in localStorage
    try {
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const cachedProfile = profiles.find(p =>
        p.username === username && p.platform === platform
      );

      if (cachedProfile) {
        console.log(`Using cached ${platform} profile from localStorage`);
        return cachedProfile;
      }
    } catch (e) {
      console.error('Error reading from localStorage:', e);
    }

    throw error;
  }
};

/**
 * Delete a profile
 * @param {string} platform - Platform name (github, linkedin, leetcode)
 * @param {string} username - Username on the platform
 * @returns {Promise<Object>} Response data
 */
export const deleteProfile = async (platform, username) => {
  try {
    // First try to delete from the API
    try {
      const response = await api.delete(`/profile/${platform}/${username}`);
      return response;
    } catch (apiError) {
      // If API fails, just remove from localStorage
      console.warn('API unavailable, removing from localStorage only');
      const profiles = JSON.parse(localStorage.getItem('profiles') || '[]');
      const filteredProfiles = profiles.filter(p =>
        !(p.username === username && p.platform === platform)
      );
      localStorage.setItem('profiles', JSON.stringify(filteredProfiles));
      return { status: 'success', message: 'Profile removed from local storage' };
    }
  } catch (error) {
    console.error(`Error deleting ${platform} profile for ${username}:`, error);
    throw error;
  }
};