/**
 * Configuration options for the Spline 3D background
 */

// Main Spline URL for production - Using direct splinecode URL format to prevent CORS
export const MAIN_SPLINE_URL = 'https://prod.spline.design/0ae66577-453d-44d4-9442-21be56fd343d/scene.splinecode';

// Fallback URL in case the main one fails - simplified scene
export const FALLBACK_SPLINE_URL = 'https://prod.spline.design/vOLBRkTlRxdUgUOD/scene.splinecode';

// Default background opacity (0-1)
export const DEFAULT_OPACITY = 0.15;

// Performance settings
export const SPLINE_OPTIONS = {
  // Custom settings as props for the Spline component
  // (These will be filtered before being passed to DOM elements)

  // If the user has a slow device, we can reduce the scene quality
  enableLowPerformanceMode: window.navigator.deviceMemory < 4, // Less than 4GB RAM

  // Disable events for background scenes to improve performance
  events: {
    click: false,
    hover: false,
    scroll: false,
    mouseDown: false,
    mouseUp: false,
    mouseMove: false,
    touchStart: false,
    touchEnd: false,
    touchMove: false,
  },

  // Load only essential assets for web
  loadOptonWhenWeb: 'light',

  // Background appearance
  background: {
    color: {
      r: 248,
      g: 250,
      b: 252,
      a: 0,
    },
  },
};

/**
 * Get the appropriate Spline URL based on device capabilities
 */
export const getSplineUrl = () => {
  // Use a simpler scene for mobile devices or low memory devices
  const isMobile = window.innerWidth < 768 ||
                  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  const isLowMemory = window.navigator.deviceMemory < 4;

  if (isMobile || isLowMemory) {
    return FALLBACK_SPLINE_URL;
  }

  return MAIN_SPLINE_URL;
};