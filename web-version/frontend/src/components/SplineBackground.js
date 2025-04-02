import React, { useState, useEffect, useRef } from 'react';
import Spline from '@splinetool/react-spline';
import {
  getSplineUrl,
  FALLBACK_SPLINE_URL,
  SPLINE_OPTIONS,
  DEFAULT_OPACITY
} from '../utils/splineConfig';

/**
 * A component that renders a Spline 3D scene as a background
 * @param {Object} props
 * @param {string} props.splineUrl - URL to the Spline scene (optional, will use config if not provided)
 * @param {React.ReactNode} props.children - Content to render over the background
 * @param {number} props.opacity - Opacity of the background (0-1)
 */
const SplineBackground = ({ splineUrl, children, opacity = DEFAULT_OPACITY }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [url, setUrl] = useState(splineUrl || getSplineUrl());
  const [useAltBackground, setUseAltBackground] = useState(false);
  const retryCount = useRef(0);

  // Handle errors and retry with alternative URLs
  useEffect(() => {
    if (error) {
      if (retryCount.current < 2) {
        console.log(`Retry attempt ${retryCount.current + 1}: Switching to alternative Spline URL`);

        // Try fallback on first retry, or disable on second retry
        if (retryCount.current === 0) {
          setUrl(FALLBACK_SPLINE_URL);
        } else {
          setUseAltBackground(true);
        }

        retryCount.current += 1;
        setError(null);
        setLoading(true);
      } else {
        // If we've tried multiple times, show the fallback UI
        console.log('Failed to load Spline background after multiple attempts');
        setUseAltBackground(true);
        setLoading(false);
      }
    }
  }, [error]);

  const handleLoad = () => {
    console.log('Spline scene loaded successfully');
    setLoading(false);
  };

  const handleError = (err) => {
    console.error('Error loading Spline scene:', err);
    setError('Failed to load 3D background');
    setLoading(false);
  };

  // Extract props that shouldn't be passed directly to DOM elements
  const {
    enableLowPerformanceMode,
    loadOptonWhenWeb,
    events,
    background,
    ...safeSplineProps
  } = SPLINE_OPTIONS;

  return (
    <div className="relative w-full">
      {/* Spline background container */}
      <div
        className="fixed top-0 left-0 w-full h-full z-0 pointer-events-none"
        style={{ opacity }}
      >
        {loading && !useAltBackground && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-50">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        )}

        {useAltBackground ? (
          // Fallback background when Spline fails
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-100">
            <div className="absolute top-0 left-0 w-96 h-96 bg-blue-200 rounded-full filter blur-3xl opacity-30"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-200 rounded-full filter blur-3xl opacity-30"></div>
          </div>
        ) : (
          // Try to load Spline scene
          <Spline
            scene={url}
            onLoad={handleLoad}
            onError={handleError}
            className="spline-canvas"
            {...safeSplineProps}
          />
        )}
      </div>

      {/* Foreground content */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export default SplineBackground;