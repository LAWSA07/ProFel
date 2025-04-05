import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="py-16 md:py-24 text-center relative overflow-hidden">
        <div className="absolute inset-0 z-0 opacity-5">
          <div className="absolute top-0 left-0 w-96 h-96 bg-blue-400 rounded-full filter blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-400 rounded-full filter blur-3xl"></div>
        </div>

        <div className="relative z-10 max-w-4xl mx-auto px-4">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6 leading-tight">
            <span className="text-blue-600">Profel:</span> Match Skills with Job Requirements
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Extract skills from developer profiles and match them with job requirements using AI-powered analysis.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/profiles"
              className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition duration-300"
            >
              Analyze Profiles
            </Link>
            <Link
              to="/matching"
              className="px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg shadow-lg border border-blue-200 hover:bg-gray-50 transition duration-300"
            >
              Match Skills
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-12 bg-gray-50 bg-opacity-50 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <div className="text-blue-600 text-4xl font-bold mb-2">100%</div>
              <div className="text-gray-700 font-medium">Accuracy in Skill Matching</div>
            </div>
            <div className="p-6">
              <div className="text-blue-600 text-4xl font-bold mb-2">50+</div>
              <div className="text-gray-700 font-medium">Programming Languages Analyzed</div>
            </div>
            <div className="p-6">
              <div className="text-blue-600 text-4xl font-bold mb-2">5 min</div>
              <div className="text-gray-700 font-medium">Average Matching Time</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16 text-gray-800">How It Works</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Profile Analysis</h3>
              <p className="text-gray-600 leading-relaxed">
                Extract skills and projects from multiple platforms using AI-powered analysis to create a comprehensive skill profile.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
                  <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Job Definition</h3>
              <p className="text-gray-600 leading-relaxed">
                Define job requirements with weighted skill importance to ensure accurate and targeted matching.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">Smart Matching</h3>
              <p className="text-gray-600 leading-relaxed">
                Match profiles to jobs with advanced algorithms that consider skill importance, proficiency, and relevance.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-gray-50 bg-opacity-60 backdrop-blur-sm">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6 text-gray-800">Ready to Find the Perfect Match?</h2>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Get started with Profel's profile analysis and job matching today.
          </p>
          <Link
            to="/profiles"
            className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition duration-300"
          >
            Get Started Now
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;