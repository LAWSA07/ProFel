import React, { useState, useEffect } from 'react';

const MatchForm = ({ profiles, jobs, onSubmit, isLoading }) => {
  const [selectedProfile, setSelectedProfile] = useState('');
  const [selectedJob, setSelectedJob] = useState('');

  // Update selected profile and job when new options become available
  useEffect(() => {
    if (profiles && profiles.length > 0 && !selectedProfile && profiles[0]) {
      setSelectedProfile(profiles[0].id || profiles[0].username || `profile-${0}`);
    }
  }, [profiles, selectedProfile]);

  useEffect(() => {
    if (jobs && jobs.length > 0 && !selectedJob && jobs[0]) {
      setSelectedJob(jobs[0].id || `job-${0}`);
    }
  }, [jobs, selectedJob]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedProfile && selectedJob) {
      onSubmit({ profileId: selectedProfile, jobId: selectedJob });
    }
  };

  // Check if we have profiles and jobs to match
  const hasOptions = profiles && profiles.length > 0 && jobs && jobs.length > 0;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Match Profile to Job</h2>

      {!hasOptions ? (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
          <p className="text-yellow-700">
            You need at least one GitHub profile and one job to perform matching.
          </p>
          <ul className="list-disc ml-5 mt-2 text-sm text-yellow-600">
            {(!profiles || profiles.length === 0) && (
              <li>Add a GitHub profile in the "GitHub Profiles" section</li>
            )}
            {(!jobs || jobs.length === 0) && (
              <li>Add a job in the "Jobs" section</li>
            )}
          </ul>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="profile" className="block text-gray-700 text-sm font-bold mb-2">
              Select Profile
            </label>
            <select
              id="profile"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={selectedProfile}
              onChange={(e) => setSelectedProfile(e.target.value)}
              disabled={isLoading || !profiles || profiles.length === 0}
              required
            >
              {profiles && profiles.map((profile, index) => {
                if (!profile) return null;
                const profileId = profile.id || profile.username || `profile-${index}`;
                const displayName = profile.name || profile.username || `Profile ${index + 1}`;

                return (
                  <option key={profileId} value={profileId}>
                    {displayName}
                  </option>
                );
              })}
            </select>
          </div>

          <div className="mb-6">
            <label htmlFor="job" className="block text-gray-700 text-sm font-bold mb-2">
              Select Job
            </label>
            <select
              id="job"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={selectedJob}
              onChange={(e) => setSelectedJob(e.target.value)}
              disabled={isLoading || !jobs || jobs.length === 0}
              required
            >
              {jobs && jobs.map((job, index) => {
                if (!job) return null;
                const jobId = job.id || `job-${index}`;
                const displayTitle = job.title || `Job ${index + 1}`;
                const company = job.company || 'Unknown';

                return (
                  <option key={jobId} value={jobId}>
                    {displayTitle} at {company}
                  </option>
                );
              })}
            </select>
          </div>

          <div className="flex items-center justify-between">
            <button
              type="submit"
              className={`bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${
                isLoading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={isLoading}
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
                'Calculate Match'
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default MatchForm;