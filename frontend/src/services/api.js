import axios from 'axios';

// Get the backend URL from environment variables or use the default
const API_URL = process.env.REACT_APP_API_URL || 'https://profel.onrender.com/api';

// Track API availability to avoid multiple failed requests
let isApiAvailable = true;
let lastApiCheckTime = 0;
const API_CHECK_INTERVAL = 30000; // 30 seconds between API availability checks

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // Reduced timeout to 10 seconds
});

// Add a request interceptor to handle common request tasks
api.interceptors.request.use(
  (config) => {
    const currentTime = Date.now();

    // Skip API calls if we know it's unavailable (unless enough time has passed)
    if (!isApiAvailable && (currentTime - lastApiCheckTime) < API_CHECK_INTERVAL) {
      console.log(`API is currently unavailable, skipping request: ${config.method.toUpperCase()} ${config.url}`);
      return Promise.reject({
        isApiUnavailableError: true,
        message: 'API is currently unavailable, using local storage instead',
        displayMessage: 'Backend server is not available, using local storage'
      });
    }

    // Reset last check time if we're trying again
    if (!isApiAvailable) {
      console.log('Attempting to reconnect to API after timeout period');
    }

    lastApiCheckTime = currentTime;
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
    // Mark API as available since we got a successful response
    isApiAvailable = true;
    console.log(`API Response: ${response.status} from ${response.config.url}`);
    // Return the response data directly
    return response.data;
  },
  (error) => {
    // Handle API errors
    let errorMessage = 'An unexpected error occurred';

    if (error.isApiUnavailableError) {
      // This is our custom error when API is known to be unavailable
      return Promise.reject(error);
    }

    if (error.response) {
      // The request was made and the server responded with a status code
      // outside of the range of 2xx
      const { status, data } = error.response;
      errorMessage = `Server error (${status}): ${data?.error || data?.message || 'Unknown error'}`;
      console.error('API Response Error:', {
        status,
        data,
        url: error.config?.url,
        method: error.config?.method
      });

      // Server is available but returned an error
      isApiAvailable = true;
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage = 'No response from server. Please check if the backend is running.';
      console.error('API No Response:', {
        request: error.request,
        url: error.config?.url,
        method: error.config?.method
      });

      // Mark API as unavailable since we couldn't connect
      isApiAvailable = false;
    } else {
      // Something happened in setting up the request that triggered an Error
      errorMessage = `Request error: ${error.message}`;
      console.error('API Setup Error:', error);

      // Mark API as unavailable for CORS errors
      if (error.message && (
          error.message.includes('Network Error') ||
          error.message.includes('CORS') ||
          error.message.includes('ERR_CONNECTION_REFUSED')
        )) {
        isApiAvailable = false;
      }
    }

    // Enhance error object with custom message
    error.displayMessage = errorMessage;

    return Promise.reject(error);
  }
);

export const checkApiAvailability = async () => {
  try {
    await axios.get(`${API_URL}/health`, { timeout: 3000 });
    isApiAvailable = true;
    return true;
  } catch (error) {
    isApiAvailable = false;
    return false;
  }
};

// Public API to check if backend is available
api.isAvailable = () => isApiAvailable;
api.checkAvailability = checkApiAvailability;

export default api;