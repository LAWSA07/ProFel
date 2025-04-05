import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="text-6xl font-bold text-blue-600 mb-4">404</div>
      <h1 className="text-3xl font-bold mb-6">Page Not Found</h1>
      <p className="text-lg text-gray-600 mb-8 text-center max-w-md">
        The page you are looking for doesn't exist or has been moved.
      </p>
      <Link
        to="/"
        className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 shadow-md transition-colors"
      >
        Go to Home
      </Link>
    </div>
  );
};

export default NotFound;