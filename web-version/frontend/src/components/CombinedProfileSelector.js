import React, { useState, useEffect } from 'react';

const CombinedProfileSelector = ({ profiles, onSelectProfiles, selectedProfiles = [] }) => {
  const [selected, setSelected] = useState(selectedProfiles.map(p => p.username));

  // Update selected profiles when the selectedProfiles prop changes
  useEffect(() => {
    setSelected(selectedProfiles.map(p => p.username));
  }, [selectedProfiles]);

  // Group profiles by platform
  const groupedProfiles = profiles.reduce((acc, profile) => {
    const platform = profile.platform || 'unknown';
    if (!acc[platform]) {
      acc[platform] = [];
    }
    acc[platform].push(profile);
    return acc;
  }, {});

  const handleCheckboxChange = (profile) => {
    const username = profile.username;
    let newSelected;

    if (selected.includes(username)) {
      // Remove from selection
      newSelected = selected.filter(u => u !== username);
    } else {
      // Add to selection
      newSelected = [...selected, username];
    }

    setSelected(newSelected);

    // Call the callback with the updated profile objects
    const newSelectedProfiles = profiles.filter(p => newSelected.includes(p.username));
    onSelectProfiles(newSelectedProfiles);
  };

  // Get platform display info
  const getPlatformInfo = (platform) => {
    switch (platform) {
      case 'github':
        return {
          name: 'GitHub',
          icon: (
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
          ),
          color: 'text-gray-800'
        };
      case 'linkedin':
        return {
          name: 'LinkedIn',
          icon: (
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          ),
          color: 'text-blue-700'
        };
      case 'leetcode':
        return {
          name: 'LeetCode',
          icon: (
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.662-1.823.662s-1.357-.195-1.824-.662l-4.332-4.363c-.467-.467-.702-1.15-.702-1.863s.235-1.357.702-1.824l4.319-4.38c.467-.467 1.125-.645 1.837-.645s1.357.195 1.823.662l2.697 2.606c.514.515 1.111.744 1.715.744 1.31 0 2.315-.915 2.315-2.301 0-.688-.254-1.329-.76-1.835l-2.747-2.687c-1.357-1.357-3.191-2.112-5.105-2.112s-3.748.755-5.105 2.112l-4.319 4.363C.963 10.562.193 12.426.193 14.407s.77 3.794 2.172 5.199l4.319 4.363c1.357 1.358 3.191 2.13 5.105 2.13s3.748-.773 5.105-2.13l2.747-2.665c.506-.506.76-1.147.76-1.836 0-1.386-1.005-2.301-2.315-2.301-.603 0-1.2.228-1.715.744l.031.03z" />
            </svg>
          ),
          color: 'text-yellow-600'
        };
      default:
        return {
          name: platform.charAt(0).toUpperCase() + platform.slice(1),
          icon: null,
          color: 'text-gray-600'
        };
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-bold mb-4">Combine Profiles</h3>

      <div className="mb-4 text-sm text-gray-600">
        <p>Select profiles from different platforms to combine their skills and experience for a more comprehensive match.</p>
      </div>

      {Object.entries(groupedProfiles).length === 0 ? (
        <div className="p-4 bg-gray-50 rounded text-center text-gray-500">
          No profiles available. Please add profiles from different platforms.
        </div>
      ) : (
        <div className="space-y-4">
          {Object.entries(groupedProfiles).map(([platform, platformProfiles]) => {
            const { name, icon, color } = getPlatformInfo(platform);
            return (
              <div key={platform} className="border rounded-lg overflow-hidden">
                <div className={`flex items-center p-3 bg-gray-50 ${color} border-b`}>
                  <div className="mr-2">{icon}</div>
                  <h4 className="font-medium">{name} Profiles</h4>
                </div>
                <div className="divide-y">
                  {platformProfiles.map(profile => (
                    <div key={profile.username} className="flex items-center p-3 hover:bg-gray-50">
                      <input
                        type="checkbox"
                        id={`profile-${profile.username}-${platform}`}
                        checked={selected.includes(profile.username)}
                        onChange={() => handleCheckboxChange(profile)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label
                        htmlFor={`profile-${profile.username}-${platform}`}
                        className="ml-3 block text-gray-700 cursor-pointer"
                      >
                        <span className="font-medium">{profile.name || profile.username}</span>
                        {profile.name && profile.username && profile.name !== profile.username && (
                          <span className="text-gray-500 text-sm ml-2">@{profile.username}</span>
                        )}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="mt-4 pt-4 border-t flex justify-between items-center">
        <div className="text-sm text-gray-600">
          {selected.length} profile{selected.length !== 1 ? 's' : ''} selected
        </div>
        {selected.length > 0 && (
          <div>
            <span className="inline-flex bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
              {selected.length} profile{selected.length !== 1 ? 's' : ''} ready to combine
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default CombinedProfileSelector;