import React, { useState, useEffect } from 'react';
import JobForm from '../components/JobForm';
import JobCard from '../components/JobCard';
import { createJob } from '../services/jobsService';

const JobsPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [createStatus, setCreateStatus] = useState({ loading: false, error: null });

  // Load jobs from localStorage on component mount
  useEffect(() => {
    loadJobsFromStorage();
  }, []);

  // Save jobs to localStorage whenever they change
  useEffect(() => {
    if (jobs.length > 0) {
      localStorage.setItem('jobs', JSON.stringify(jobs));
    }
  }, [jobs]);

  const loadJobsFromStorage = () => {
    try {
      const savedJobs = localStorage.getItem('jobs');
      if (savedJobs) {
        setJobs(JSON.parse(savedJobs));
      }
    } catch (err) {
      console.error('Error loading jobs from storage:', err);
      setError('Failed to load saved jobs');
    }
  };

  const handleCreateJob = async (jobData) => {
    try {
      setCreateStatus({ loading: true, error: null });

      // Try to use the API first
      let createdJob;
      try {
        createdJob = await createJob(jobData);
      } catch (apiError) {
        console.error('API error, falling back to local storage:', apiError);

        // Fall back to local storage if API fails
        createdJob = {
          ...jobData,
          id: `job_${Date.now()}`,
          created_at: new Date().toISOString(),
          level: calculateJobLevel(jobData.title),
          skills: parseSkills(jobData.skills_text)
        };
      }

      // Add to jobs list
      setJobs(prevJobs => [...prevJobs, createdJob]);

      setCreateStatus({ loading: false, error: null });
    } catch (err) {
      setCreateStatus({
        loading: false,
        error: err.displayMessage || 'Failed to create job'
      });
      console.error('Error creating job:', err);
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        setLoading(true);

        // Remove from jobs list in state
        setJobs(prevJobs => prevJobs.filter(job => job.id !== jobId));

        // Also remove from localStorage
        const savedJobs = JSON.parse(localStorage.getItem('jobs') || '[]');
        const updatedJobs = savedJobs.filter(job => job.id !== jobId);
        localStorage.setItem('jobs', JSON.stringify(updatedJobs));

        setLoading(false);
      } catch (err) {
        setError(err.displayMessage || 'Failed to delete job');
        setLoading(false);
        console.error('Error deleting job:', err);
      }
    }
  };

  // Helper function to calculate job level from title
  const calculateJobLevel = (title) => {
    const lowerTitle = title.toLowerCase();

    if (lowerTitle.includes('senior') || lowerTitle.includes('lead') ||
        lowerTitle.includes('architect') || lowerTitle.includes('manager')) {
      return 'senior';
    } else if (lowerTitle.includes('junior') || lowerTitle.includes('intern') ||
               lowerTitle.includes('assistant')) {
      return 'entry';
    } else {
      return 'mid';
    }
  };

  // Helper function to parse skills from comma-separated text
  const parseSkills = (skillsText) => {
    if (!skillsText) return [];

    return skillsText.split(',')
      .map((skill, index, array) => {
        const name = skill.trim();
        if (!name) return null;

        // Calculate importance based on position (earlier skills are more important)
        // First skill has importance 1.0, and we gradually decrease
        // The formula ensures that even with many skills, we don't go below 0.3
        const totalSkills = array.length;
        const importance = Math.max(0.3, 1 - (index * 0.7 / (totalSkills || 1)));

        return {
          name,
          importance: Math.round(importance * 10) / 10, // Round to 1 decimal place
          required: index < 3, // Make the first 3 skills required
          description: `Skill in ${name} is ${index < 3 ? 'essential' : 'beneficial'} for this role`
        };
      })
      .filter(Boolean); // Remove empty skills
  };

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">Jobs</h1>

      {/* Error display */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 border-l-4 border-red-500 text-red-700">
          <p>{error}</p>
        </div>
      )}

      {/* Job form */}
      <div className="mb-8">
        <JobForm
          onSubmit={handleCreateJob}
          isLoading={createStatus.loading}
        />

        {createStatus.error && (
          <div className="mt-4 p-3 bg-red-100 border-l-4 border-red-500 text-red-700">
            <p>{createStatus.error}</p>
          </div>
        )}
      </div>

      {/* Jobs listing */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Job Listings</h2>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : jobs.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 text-center">
            <p className="text-gray-500">
              No jobs yet. Add one using the form above.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {jobs.map((job) => (
              <div key={job.id} className="relative">
                <JobCard job={job} />
                <button
                  onClick={() => handleDeleteJob(job.id)}
                  className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1"
                  aria-label="Delete job"
                  title="Delete job"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobsPage;