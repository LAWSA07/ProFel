import React, { useState, useEffect } from 'react';

const ProfileForm = ({ onSubmit, isLoading, platform = 'github', disabled = false }) => {
  const [username, setUsername] = useState('');
  const [formConfig, setFormConfig] = useState({
    title: 'Fetch Profile',
    label: 'Username',
    placeholder: 'Enter username',
    examples: 'Example: user123',
    icon: null
  });

  // Configure form based on platform
  useEffect(() => {
    switch (platform) {
      case 'github':
        setFormConfig({
          title: 'Fetch GitHub Profile',
          label: 'GitHub Username',
          placeholder: 'Enter GitHub username',
          examples: 'Example: octocat, torvalds, etc.',
          icon: (
            <svg className="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
          )
        });
        break;
      case 'linkedin':
        setFormConfig({
          title: 'Fetch LinkedIn Profile',
          label: 'LinkedIn Username or URL',
          placeholder: 'Enter LinkedIn username or profile URL',
          examples: 'Example: johndoe or linkedin.com/in/johndoe',
          icon: (
            <svg className="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
            </svg>
          )
        });
        break;
      case 'leetcode':
        setFormConfig({
          title: 'Fetch LeetCode Profile',
          label: 'LeetCode Username',
          placeholder: 'Enter LeetCode username',
          examples: 'Example: leetcoder42, codingmaster, etc.',
          icon: (
            <svg className="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.662-1.823.662s-1.357-.195-1.824-.662l-4.332-4.363c-.467-.467-.702-1.15-.702-1.863s.235-1.357.702-1.824l4.319-4.38c.467-.467 1.125-.645 1.837-.645s1.357.195 1.823.662l2.697 2.606c.514.515 1.111.744 1.715.744 1.31 0 2.315-.915 2.315-2.301 0-.688-.254-1.329-.76-1.835l-2.747-2.687c-1.357-1.357-3.191-2.112-5.105-2.112s-3.748.755-5.105 2.112l-4.319 4.363C.963 10.562.193 12.426.193 14.407s.77 3.794 2.172 5.199l4.319 4.363c1.357 1.358 3.191 2.13 5.105 2.13s3.748-.773 5.105-2.13l2.747-2.665c.506-.506.76-1.147.76-1.836 0-1.386-1.005-2.301-2.315-2.301-.603 0-1.2.228-1.715.744l.031.03z" />
            </svg>
          )
        });
        break;
      case 'codeforces':
        setFormConfig({
          title: 'Fetch Codeforces Profile',
          label: 'Codeforces Handle',
          placeholder: 'Enter Codeforces handle',
          examples: 'Example: tourist, petr, etc.',
          icon: (
            <svg className="h-5 w-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M4.5 7.5C5.328 7.5 6 8.172 6 9v10.5c0 .828-.672 1.5-1.5 1.5h-3C.672 21 0 20.328 0 19.5V9c0-.828.672-1.5 1.5-1.5h3zm19.5 0c0-2.485-2.015-4.5-4.5-4.5S15 5.015 15 7.5v2.25h1.5c.828 0 1.5.672 1.5 1.5v8.25c0 .828-.672 1.5-1.5 1.5h-3c-.828 0-1.5-.672-1.5-1.5V11.25c0-.828.672-1.5 1.5-1.5H15V7.5C15 6.12 16.12 5 17.5 5S20 6.12 20 7.5V9h1.5c.828 0 1.5.672 1.5 1.5v9c0 .828-.672 1.5-1.5 1.5h-3c-.828 0-1.5-.672-1.5-1.5v-9c0-.828.672-1.5 1.5-1.5H21V7.5z" />
            </svg>
          )
        });
        break;
      default:
        setFormConfig({
          title: 'Fetch Profile',
          label: 'Username',
          placeholder: 'Enter username',
          examples: 'Example: user123',
          icon: null
        });
    }
  }, [platform]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      onSubmit(username.trim());
    }
  };

  return (
    <div className={`bg-white p-8 rounded-lg shadow-lg glass-effect border border-gray-200 ${disabled ? 'opacity-60' : ''}`}>
      <div className="flex items-center mb-6 pb-3 border-b">
        <div className="text-blue-600 mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-800">{formConfig.title}</h2>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="username" className="block text-gray-700 font-medium mb-2">
            {formConfig.label}
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {formConfig.icon}
            </div>
            <input
              type="text"
              id="username"
              className="shadow-sm border border-gray-300 rounded-lg w-full py-3 px-4 pl-10 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder={formConfig.placeholder}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading || disabled}
              required
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {formConfig.examples}
          </p>
          {disabled && (
            <p className="text-xs text-orange-500 mt-2">
              This platform integration is coming soon!
            </p>
          )}
        </div>

        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-500 italic">
            This may take a few seconds
          </p>
          <button
            type="submit"
            className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-all ${
              (isLoading || disabled) ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={isLoading || disabled}
          >
            {isLoading ? (
              <div className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </div>
            ) : (
              'Fetch Profile'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProfileForm;