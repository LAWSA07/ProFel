import React, { useState, useEffect } from 'react';
import ProfileForm from '../components/ProfileForm';
import ProfileCard from '../components/ProfileCard';
import { fetchProfile } from '../services/githubService';

const ProfilesPage = () => {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fetchStatus, setFetchStatus] = useState({ loading: false, error: null });
  const [activePlatform, setActivePlatform] = useState('github');

  // Load profiles from localStorage on component mount
  useEffect(() => {
    loadProfilesFromStorage();
  }, []);

  // Save profiles to localStorage whenever they change
  useEffect(() => {
    if (profiles.length > 0) {
      localStorage.setItem('profiles', JSON.stringify(profiles));
    }
  }, [profiles]);

  const loadProfilesFromStorage = () => {
    try {
      const savedProfiles = localStorage.getItem('profiles');
      if (savedProfiles) {
        setProfiles(JSON.parse(savedProfiles));
      }
    } catch (err) {
      console.error('Error loading profiles from storage:', err);
      setError('Failed to load saved profiles');
    }
  };

  const handleFetchProfile = async (username) => {
    try {
      setFetchStatus({ loading: true, error: null });

      let fetchedProfile;

      // Handle different platform fetches (only GitHub implemented for now)
      switch (activePlatform) {
        case 'github':
          fetchedProfile = await fetchProfile(username);
          break;
        case 'linkedin':
          // Future implementation
          fetchedProfile = {
            platform: 'linkedin',
            username,
            name: username,
            bio: 'LinkedIn profile data will be available in a future update',
            _placeholder: true
          };
          break;
        case 'leetcode':
          // Future implementation
          fetchedProfile = {
            platform: 'leetcode',
            username,
            name: username,
            bio: 'LeetCode profile data will be available in a future update',
            _placeholder: true
          };
          break;
        case 'codeforces':
          // Future implementation
          fetchedProfile = {
            platform: 'codeforces',
            username,
            name: username,
            bio: 'Codeforces profile data will be available in a future update',
            _placeholder: true
          };
          break;
        default:
          throw new Error(`Unsupported platform: ${activePlatform}`);
      }

      // Set platform type on the profile
      fetchedProfile.platform = activePlatform;

      // Add to profiles list
      setProfiles(prevProfiles => {
        // Check if profile already exists, replace it if so
        const existingIndex = prevProfiles.findIndex(
          p => p?.username?.toLowerCase() === username.toLowerCase() &&
               p?.platform === activePlatform
        );

        if (existingIndex >= 0) {
          const updatedProfiles = [...prevProfiles];
          updatedProfiles[existingIndex] = fetchedProfile;
          return updatedProfiles;
        } else {
          return [...prevProfiles, fetchedProfile];
        }
      });

      setFetchStatus({ loading: false, error: null });
    } catch (err) {
      setFetchStatus({
        loading: false,
        error: err.displayMessage || `Failed to fetch ${activePlatform} profile for "${username}"`
      });
      console.error(`Error fetching ${activePlatform} profile:`, err);
    }
  };

  const handleDeleteProfile = async (profileId, platform) => {
    if (!profileId) return;

    if (window.confirm(`Are you sure you want to delete this ${platform} profile?`)) {
      try {
        setLoading(true);
        // We'll just remove it from our local state for now
        // Backend deletion can be implemented later
        setProfiles(prevProfiles =>
          prevProfiles.filter(p =>
            !(p?.username?.toLowerCase() === profileId.toLowerCase() && p?.platform === platform)
          )
        );

        // Also remove from localStorage
        const savedProfiles = JSON.parse(localStorage.getItem('profiles') || '[]');
        const updatedProfiles = savedProfiles.filter(
          p => !(p?.username?.toLowerCase() === profileId.toLowerCase() && p?.platform === platform)
        );
        localStorage.setItem('profiles', JSON.stringify(updatedProfiles));

        setLoading(false);
      } catch (err) {
        setError(err.displayMessage || `Failed to delete ${platform} profile for "${profileId}"`);
        setLoading(false);
        console.error('Error deleting profile:', err);
      }
    }
  };

  // Filter profiles by the active platform
  const filteredProfiles = profiles.filter(p => p?.platform === activePlatform);

  // Platform options with display details
  const platforms = [
    {
      id: 'github',
      name: 'GitHub',
      icon: (
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
        </svg>
      ),
      description: "Pull your GitHub profile to highlight your repositories and coding skills.",
      isImplemented: true
    },
    {
      id: 'linkedin',
      name: 'LinkedIn',
      icon: (
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      ),
      description: "Import your LinkedIn profile to showcase your professional experience and network.",
      comingSoon: true
    },
    {
      id: 'leetcode',
      name: 'LeetCode',
      icon: (
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.662-1.823.662s-1.357-.195-1.824-.662l-4.332-4.363c-.467-.467-.702-1.15-.702-1.863s.235-1.357.702-1.824l4.319-4.38c.467-.467 1.125-.645 1.837-.645s1.357.195 1.823.662l2.697 2.606c.514.515 1.111.744 1.715.744 1.31 0 2.315-.915 2.315-2.301 0-.688-.254-1.329-.76-1.835l-2.747-2.687c-1.357-1.357-3.191-2.112-5.105-2.112s-3.748.755-5.105 2.112l-4.319 4.363C.963 10.562.193 12.426.193 14.407s.77 3.794 2.172 5.199l4.319 4.363c1.357 1.358 3.191 2.13 5.105 2.13s3.748-.773 5.105-2.13l2.747-2.665c.506-.506.76-1.147.76-1.836 0-1.386-1.005-2.301-2.315-2.301-.603 0-1.2.228-1.715.744l.031.03z" />
        </svg>
      ),
      description: "Connect your LeetCode account to display your problem-solving abilities and contest rankings.",
      comingSoon: true
    },
    {
      id: 'codeforces',
      name: 'Codeforces',
      icon: (
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path d="M4.5 7.5C5.328 7.5 6 8.172 6 9v10.5c0 .828-.672 1.5-1.5 1.5h-3C.672 21 0 20.328 0 19.5V9c0-.828.672-1.5 1.5-1.5h3zm19.5 0c0-2.485-2.015-4.5-4.5-4.5S15 5.015 15 7.5v2.25h1.5c.828 0 1.5.672 1.5 1.5v8.25c0 .828-.672 1.5-1.5 1.5h-3c-.828 0-1.5-.672-1.5-1.5v-9c0-.828.672-1.5 1.5-1.5H21V7.5z" />
        </svg>
      ),
      description: "Integrate your Codeforces profile to showcase your competitive programming achievements.",
      comingSoon: true
    }
  ];

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">Developer Profiles</h1>

      {/* Platform selection tabs */}
      <div className="mb-8">
        <div className="border-b border-gray-200">
          <ul className="flex flex-wrap -mb-px text-sm font-medium text-center">
            {platforms.map(platform => (
              <li key={platform.id} className="mr-2">
                <button
                  onClick={() => setActivePlatform(platform.id)}
                  className={`inline-flex items-center justify-center p-4 border-b-2 rounded-t-lg group ${
                    activePlatform === platform.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent hover:text-gray-600 hover:border-gray-300'
                  } ${platform.comingSoon ? 'opacity-60 cursor-not-allowed' : ''}`}
                  disabled={platform.comingSoon}
                >
                  {platform.icon}
                  <span className="ml-2">{platform.name}</span>
                  {platform.comingSoon && (
                    <span className="ml-2 px-2 py-0.5 text-xs bg-gray-200 rounded-full">Coming Soon</span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Platform description */}
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0 text-blue-600 mt-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="ml-3 text-sm text-blue-700">
              {platforms.find(p => p.id === activePlatform)?.description}
              {platforms.find(p => p.id === activePlatform)?.comingSoon &&
                " This integration is coming soon. Please check back later!"}
            </p>
          </div>
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 border-l-4 border-red-500 text-red-700">
          <p>{error}</p>
        </div>
      )}

      {/* Profile form */}
      <div className="mb-8">
        <ProfileForm
          onSubmit={handleFetchProfile}
          isLoading={fetchStatus.loading}
          platform={activePlatform}
          disabled={platforms.find(p => p.id === activePlatform)?.comingSoon}
        />

        {fetchStatus.error && (
          <div className="mt-4 p-3 bg-red-100 border-l-4 border-red-500 text-red-700">
            <p>{fetchStatus.error}</p>
          </div>
        )}
      </div>

      {/* Profiles listing */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Your {platforms.find(p => p.id === activePlatform)?.name} Profiles</h2>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : filteredProfiles.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 text-center">
            <p className="text-gray-500">
              No {platforms.find(p => p.id === activePlatform)?.name} profiles yet.
              {!platforms.find(p => p.id === activePlatform)?.comingSoon
                ? " Add one using the form above."
                : " This platform integration is coming soon!"}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProfiles.map((profile, index) => {
              // Handle potentially invalid profiles
              if (!profile) return null;

              const profileId = profile.username || profile.id || `profile-${index}`;

              return (
                <div key={`${profile.platform}-${profileId}`} className="relative">
                  <ProfileCard profile={profile} />
                  <button
                    onClick={() => handleDeleteProfile(profileId, profile.platform)}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1"
                    aria-label="Delete profile"
                    title="Delete profile"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilesPage;