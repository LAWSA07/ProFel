import api from './api';

/**
 * Get all jobs
 * @returns {Promise<Array>} Array of jobs
 */
export const getAllJobs = async () => {
  try {
    const response = await api.get('/jobs');
    return response.data || [];
  } catch (error) {
    console.error('Error fetching jobs:', error);
    throw error;
  }
};

/**
 * Get a specific job
 * @param {string} jobId - Job ID
 * @returns {Promise<Object>} Job data
 */
export const getJob = async (jobId) => {
  try {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching job ${jobId}:`, error);
    throw error;
  }
};

/**
 * Create a new job
 * @param {Object} jobData - Job data
 * @returns {Promise<Object>} Created job data
 */
export const createJob = async (jobData) => {
  try {
    const response = await api.post('/jobs', jobData);

    // Check if response structure is as expected
    if (response && response.job) {
      return response.job;
    } else if (response && typeof response === 'object') {
      // If response doesn't have job property but is an object,
      // assume the response itself is the job
      return {
        ...response,
        // Ensure required fields exist
        id: response.id || `job_${Date.now()}`,
        title: response.title || jobData.title || 'Untitled Job',
        company: response.company || jobData.company || 'Unknown Company'
      };
    }

    // If response is not as expected, create a fallback job
    console.warn('API returned unexpected response format, using fallback', response);
    return {
      ...jobData,
      id: `job_${Date.now()}`,
      created_at: new Date().toISOString()
    };
  } catch (error) {
    console.error('Error creating job:', error);
    throw error;
  }
};

/**
 * Update an existing job
 * @param {string} jobId - Job ID
 * @param {Object} jobData - Updated job data
 * @returns {Promise<Object>} Updated job data
 */
export const updateJob = async (jobId, jobData) => {
  try {
    const response = await api.put(`/jobs/${jobId}`, jobData);
    return response.data;
  } catch (error) {
    console.error(`Error updating job ${jobId}:`, error);
    throw error;
  }
};

/**
 * Delete a job
 * @param {string} jobId - Job ID
 * @returns {Promise<Object>} Response data
 */
export const deleteJob = async (jobId) => {
  try {
    const response = await api.delete(`/jobs/${jobId}`);
    return response;
  } catch (error) {
    console.error(`Error deleting job ${jobId}:`, error);
    throw error;
  }
};