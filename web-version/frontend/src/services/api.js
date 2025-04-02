import axios from 'axios';

// Get the backend URL from environment variables or use the default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// Add a request interceptor to handle common request tasks
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle common response tasks
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} from ${response.config.url}`);
    // Return the response data directly
    return response.data;
  },
  (error) => {
    // Handle API errors
    let errorMessage = 'An unexpected error occurred';

    if (error.response) {
      // The request was made and the server responded with a status code
      // outside of the range of 2xx
      const { status, data } = error.response;
      errorMessage = `Server error (${status}): ${data.error || data.message || 'Unknown error'}`;
      console.error('API Response Error:', {
        status,
        data,
        url: error.config.url,
        method: error.config.method
      });
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage = 'No response from server. Please check if the backend is running.';
      console.error('API No Response:', {
        request: error.request,
        url: error.config?.url,
        method: error.config?.method
      });
    } else {
      // Something happened in setting up the request that triggered an Error
      errorMessage = `Request error: ${error.message}`;
      console.error('API Setup Error:', error);
    }

    // Enhance error object with custom message
    error.displayMessage = errorMessage;

    return Promise.reject(error);
  }
);

export default api;