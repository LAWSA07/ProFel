import React from 'react';

const JobCard = ({ job }) => {
  if (!job) return null;

  // Helper function to get color based on importance
  const getImportanceColor = (importance) => {
    if (importance >= 0.8) return 'bg-red-100 text-red-800';
    if (importance >= 0.6) return 'bg-orange-100 text-orange-800';
    if (importance >= 0.4) return 'bg-yellow-100 text-yellow-800';
    return 'bg-blue-100 text-blue-800';
  };

  return (
    <div className="bg-white glass-effect rounded-lg shadow-lg overflow-hidden border border-gray-200 transition-all hover:shadow-xl">
      <div className="p-6">
        <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">{job.title}</h2>
          <div className="text-gray-600 font-medium">{job.company}</div>
        </div>

        {job.location && (
          <div className="flex items-center text-gray-600 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{job.location}</span>
          </div>
        )}

        {job.level && (
          <div className="mb-4">
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold backdrop-blur-sm ${
              job.level === 'senior' ? 'bg-purple-100 text-purple-800' :
              job.level === 'mid' ? 'bg-blue-100 text-blue-800' :
              'bg-green-100 text-green-800'
            }`}>
              {job.level.charAt(0).toUpperCase() + job.level.slice(1)}-level
            </span>
          </div>
        )}

        {job.description && (
          <div className="mb-5">
            <div className="flex items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-md font-semibold text-gray-700">Job Description</h3>
            </div>
            <p className="text-gray-600 pl-7">{job.description}</p>
          </div>
        )}

        {/* Skills section */}
        {job.skills && job.skills.length > 0 && (
          <div className="mb-2">
            <div className="flex items-center mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <h3 className="text-md font-semibold text-gray-700">Required Skills</h3>
            </div>
            <div className="flex flex-wrap gap-2 pl-7">
              {job.skills.map((skill, index) => {
                const skillObj = typeof skill === 'string' ? { name: skill, importance: 0.5 } : skill;
                const importance = skillObj.importance || 0.5;

                return (
                  <div
                    key={index}
                    className="relative group"
                  >
                    <span className={`${getImportanceColor(importance)} rounded-full px-3 py-1 text-sm backdrop-blur-sm transition-all hover:shadow-md`}>
                      {skillObj.name}
                      {importance && <span className="ml-1 font-bold">({Math.round(importance * 100)}%)</span>}
                    </span>
                    <div className="absolute hidden group-hover:block bottom-full left-1/2 transform -translate-x-1/2 mb-1 p-2 bg-gray-800 text-white text-xs rounded whitespace-nowrap z-10 backdrop-blur-sm">
                      <div>Importance: {Math.round(importance * 100)}%</div>
                      {skillObj.required && <div>Status: Required</div>}
                      {skillObj.description && <div className="mt-1">{skillObj.description}</div>}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Created date */}
        {job.created_at && (
          <div className="mt-5 pt-4 border-t border-gray-200 flex items-center text-xs text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Posted: {new Date(job.created_at).toLocaleDateString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobCard;