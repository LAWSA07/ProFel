import React, { useState } from 'react';

const JobForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    skills_text: '',
    location: 'Remote'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.title && formData.company && formData.skills_text) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg glass-effect border border-gray-200">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-3">Add New Job</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="title" className="block text-gray-700 font-medium mb-2">
            Job Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            className="shadow-sm border border-gray-300 rounded-lg w-full py-3 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="e.g. Senior Frontend Developer"
            value={formData.title}
            onChange={handleChange}
            disabled={isLoading}
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="company" className="block text-gray-700 font-medium mb-2">
            Company
          </label>
          <input
            type="text"
            id="company"
            name="company"
            className="shadow-sm border border-gray-300 rounded-lg w-full py-3 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="e.g. TechCorp Inc."
            value={formData.company}
            onChange={handleChange}
            disabled={isLoading}
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="location" className="block text-gray-700 font-medium mb-2">
            Location
          </label>
          <input
            type="text"
            id="location"
            name="location"
            className="shadow-sm border border-gray-300 rounded-lg w-full py-3 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="e.g. Remote, New York, NY"
            value={formData.location}
            onChange={handleChange}
            disabled={isLoading}
          />
        </div>

        <div className="mb-8">
          <label htmlFor="skills_text" className="block text-gray-700 font-medium mb-2">
            Required Skills (comma-separated)
          </label>
          <textarea
            id="skills_text"
            name="skills_text"
            className="shadow-sm border border-gray-300 rounded-lg w-full py-3 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="e.g. JavaScript, React, TypeScript, Redux"
            value={formData.skills_text}
            onChange={handleChange}
            disabled={isLoading}
            rows={3}
            required
          />
          <p className="text-sm text-gray-500 mt-2 italic">
            List skills in order of importance, with most important skills first.
          </p>
        </div>

        <div className="flex items-center justify-end">
          <button
            type="submit"
            className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-all ${
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
              'Create Job'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default JobForm;