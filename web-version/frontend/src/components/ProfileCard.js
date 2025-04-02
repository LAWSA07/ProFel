import React from 'react';

const ProfileCard = ({ profile }) => {
  if (!profile) return null;

  // Get platform-specific profile URL
  const getProfileUrl = (profile) => {
    switch (profile.platform) {
      case 'github':
        return `https://github.com/${profile.username}`;
      case 'linkedin':
        // Handle both formats: username or linkedin.com/in/username
        if (profile.username.includes('linkedin.com/')) {
          return profile.username.startsWith('http') ? profile.username : `https://${profile.username}`;
        }
        return `https://linkedin.com/in/${profile.username}`;
      case 'leetcode':
        return `https://leetcode.com/${profile.username}`;
      case 'codeforces':
        return `https://codeforces.com/profile/${profile.username}`;
      default:
        return '#';
    }
  };

  // Get platform-specific icon
  const PlatformIcon = ({ platform }) => {
    switch (platform) {
      case 'github':
        return (
          <svg className="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="currentColor">
            <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
          </svg>
        );
      case 'linkedin':
        return (
          <svg className="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
          </svg>
        );
      case 'leetcode':
        return (
          <svg className="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="currentColor">
            <path d="M16.102 17.93l-2.697 2.607c-.466.467-1.111.662-1.823.662s-1.357-.195-1.824-.662l-4.332-4.363c-.467-.467-.702-1.15-.702-1.863s.235-1.357.702-1.824l4.319-4.38c.467-.467 1.125-.645 1.837-.645s1.357.195 1.823.662l2.697 2.606c.514.515 1.111.744 1.715.744 1.31 0 2.315-.915 2.315-2.301 0-.688-.254-1.329-.76-1.835l-2.747-2.687c-1.357-1.357-3.191-2.112-5.105-2.112s-3.748.755-5.105 2.112l-4.319 4.363C.963 10.562.193 12.426.193 14.407s.77 3.794 2.172 5.199l4.319 4.363c1.357 1.358 3.191 2.13 5.105 2.13s3.748-.773 5.105-2.13l2.747-2.665c.506-.506.76-1.147.76-1.836 0-1.386-1.005-2.301-2.315-2.301-.603 0-1.2.228-1.715.744l.031.03z" />
          </svg>
        );
      case 'codeforces':
        return (
          <svg className="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="currentColor">
            <path d="M4.5 7.5C5.328 7.5 6 8.172 6 9v10.5c0 .828-.672 1.5-1.5 1.5h-3C.672 21 0 20.328 0 19.5V9c0-.828.672-1.5 1.5-1.5h3zm19.5 0c0-2.485-2.015-4.5-4.5-4.5S15 5.015 15 7.5v2.25h1.5c.828 0 1.5.672 1.5 1.5v8.25c0 .828-.672 1.5-1.5 1.5h-3c-.828 0-1.5-.672-1.5-1.5v-9c0-.828.672-1.5 1.5-1.5H21V7.5z" />
          </svg>
        );
      default:
        return null;
    }
  };

  // Get platform badge style
  const getPlatformBadgeStyle = (platform) => {
    switch (platform) {
      case 'github':
        return 'bg-gray-800 text-white';
      case 'linkedin':
        return 'bg-blue-700 text-white';
      case 'leetcode':
        return 'bg-yellow-600 text-white';
      case 'codeforces':
        return 'bg-red-600 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  // Show "Coming Soon" badge for placeholder profiles
  const isPlaceholder = profile._placeholder === true;

  return (
    <div className="bg-white glass-effect rounded-lg shadow-lg overflow-hidden border border-gray-200 transition-all hover:shadow-xl">
      <div className="p-6">
        {/* Platform badge */}
        <div className="flex justify-between items-center mb-4">
          <span
            className={`text-xs font-bold uppercase px-2 py-1 rounded-full ${getPlatformBadgeStyle(profile.platform)}`}
          >
            {profile.platform}
          </span>

          {isPlaceholder && (
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              Coming Soon
            </span>
          )}
        </div>

        <div className="flex items-center mb-4">
          {profile.avatar_url && (
            <img
              src={profile.avatar_url}
              alt={profile.name || profile.username}
              className="w-12 h-12 rounded-full mr-4 border-2 border-blue-500"
            />
          )}
          <div>
            <h2 className="text-xl font-bold text-gray-800">
              {profile.name || profile.username}
            </h2>
            {profile.username && (
              <a
                href={getProfileUrl(profile)}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline flex items-center"
              >
                <PlatformIcon platform={profile.platform} />
                @{profile.username}
              </a>
            )}
          </div>
        </div>

        {profile.bio && (
          <div className="flex items-start mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-600">{profile.bio}</p>
          </div>
        )}

        {profile.location && (
          <div className="flex items-center text-gray-600 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{profile.location}</span>
          </div>
        )}

        {/* Platform-specific sections */}
        {profile.platform === 'github' && (
          <>
            {/* Skills section */}
            {profile.skills && profile.skills.length > 0 && (
              <div className="mb-5">
                <div className="flex items-center mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  <h3 className="text-md font-semibold text-gray-700">Technical Skills</h3>
                </div>
                <div className="flex flex-wrap gap-2 pl-7">
                  {profile.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm backdrop-blur-sm transition-all hover:shadow-md"
                    >
                      {typeof skill === 'string' ? skill : skill.name}
                      {skill.proficiency && ` (${Math.round(skill.proficiency * 100)}%)`}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Projects section */}
            {profile.projects && profile.projects.length > 0 && (
              <div className="mb-5">
                <div className="flex items-center mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                  <h3 className="text-md font-semibold text-gray-700">Projects</h3>
                </div>
                <div className="space-y-3 pl-7">
                  {profile.projects.slice(0, 3).map((project, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-3 py-1">
                      <div className="flex justify-between items-center">
                        <h4 className="font-medium text-gray-800">{project.name}</h4>
                        {project.url && (
                          <a
                            href={project.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 flex items-center text-sm"
                          >
                            View
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                          </a>
                        )}
                      </div>
                      {project.description && (
                        <p className="text-sm text-gray-600 mt-1">{project.description}</p>
                      )}
                      {project.technologies && project.technologies.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {project.technologies.map((tech, techIndex) => (
                            <span key={techIndex} className="text-xs bg-gray-100 text-gray-800 px-2 py-0.5 rounded backdrop-blur-sm">
                              {tech}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                  {profile.projects.length > 3 && (
                    <div className="text-sm text-gray-500 italic pl-3">
                      + {profile.projects.length - 3} more projects
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* GitHub Stats section */}
            {profile.github_stats && (
              <div className="mt-5 pt-4 border-t border-gray-200">
                <div className="flex items-center mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <h3 className="text-md font-semibold text-gray-700">GitHub Stats</h3>
                </div>
                <div className="grid grid-cols-3 gap-3 pl-7">
                  <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                    <div className="font-bold text-center text-blue-600">{profile.github_stats.repositories || 0}</div>
                    <div className="text-xs text-center text-gray-500">Repositories</div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                    <div className="font-bold text-center text-blue-600">{profile.github_stats.followers || 0}</div>
                    <div className="text-xs text-center text-gray-500">Followers</div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                    <div className="font-bold text-center text-blue-600">{profile.github_stats.stars || 0}</div>
                    <div className="text-xs text-center text-gray-500">Stars</div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* LeetCode specific sections */}
        {profile.platform === 'leetcode' && profile.leetcode_stats && (
          <div className="mt-5 pt-4 border-t border-gray-200">
            <div className="flex items-center mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <h3 className="text-md font-semibold text-gray-700">LeetCode Stats</h3>
            </div>
            <div className="grid grid-cols-3 gap-3 pl-7">
              <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                <div className="font-bold text-center text-green-600">{profile.leetcode_stats.easy_solved || 0}</div>
                <div className="text-xs text-center text-gray-500">Easy Problems</div>
              </div>
              <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                <div className="font-bold text-center text-yellow-600">{profile.leetcode_stats.medium_solved || 0}</div>
                <div className="text-xs text-center text-gray-500">Medium Problems</div>
              </div>
              <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                <div className="font-bold text-center text-red-600">{profile.leetcode_stats.hard_solved || 0}</div>
                <div className="text-xs text-center text-gray-500">Hard Problems</div>
              </div>
            </div>
          </div>
        )}

        {/* Codeforces specific sections */}
        {profile.platform === 'codeforces' && profile.codeforces_stats && (
          <div className="mt-5 pt-4 border-t border-gray-200">
            <div className="flex items-center mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <h3 className="text-md font-semibold text-gray-700">Codeforces Stats</h3>
            </div>
            <div className="grid grid-cols-2 gap-3 pl-7">
              <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                <div className="font-bold text-center text-purple-600">{profile.codeforces_stats.rating || 0}</div>
                <div className="text-xs text-center text-gray-500">Rating</div>
              </div>
              <div className="bg-gray-50 p-3 rounded backdrop-blur-sm shadow-sm transition-all hover:shadow-md">
                <div className="font-bold text-center text-purple-600">{profile.codeforces_stats.rank || "Unranked"}</div>
                <div className="text-xs text-center text-gray-500">Rank</div>
              </div>
            </div>
          </div>
        )}

        {/* Coming soon section for placeholder profiles */}
        {isPlaceholder && (
          <div className="mt-5 p-4 bg-blue-50 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0 text-blue-600 mt-0.5">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">Coming Soon</h3>
                <div className="mt-1 text-sm text-blue-700">
                  <p>Support for {profile.platform} profiles is coming soon!</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileCard;