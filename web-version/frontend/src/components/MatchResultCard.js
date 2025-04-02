import React, { useState } from 'react';

const MatchResultCard = ({ matchResult }) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!matchResult) return null;

  // Determine color based on match percentage
  const getMatchColor = (percentage) => {
    if (percentage >= 85) return 'bg-green-500';
    if (percentage >= 70) return 'bg-blue-500';
    if (percentage >= 50) return 'bg-yellow-500';
    if (percentage >= 30) return 'bg-orange-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-white glass-effect rounded-lg shadow-md overflow-hidden border border-gray-200">
      <div className="p-4">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-800">{matchResult.profile_name}</h2>
            <div className="text-gray-600">
              {matchResult.job_title} at {matchResult.company}
            </div>
          </div>

          <div className="mt-2 sm:mt-0 flex items-center">
            <div className="h-16 w-16 rounded-full flex items-center justify-center text-white font-bold text-lg mr-3"
                 style={{ background: getMatchColor(matchResult.overall_match) }}>
              {Math.round(matchResult.overall_match)}%
            </div>
          </div>
        </div>

        {/* Recommendation */}
        <div className="mb-4 p-3 bg-gray-50 bg-opacity-75 backdrop-blur-sm rounded-md">
          <h3 className="font-medium text-gray-700 mb-1">Recommendation</h3>
          <p className="text-gray-600">{matchResult.recommendation}</p>
        </div>

        {/* Strengths */}
        {matchResult.strengths && matchResult.strengths.length > 0 && (
          <div className="mb-4">
            <h3 className="font-medium text-gray-700 mb-1">Key Strengths</h3>
            <div className="flex flex-wrap gap-2">
              {matchResult.strengths.map((strength, index) => (
                <span
                  key={index}
                  className="bg-green-100 text-green-800 rounded-full px-3 py-1 text-sm backdrop-blur-sm"
                >
                  {strength}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Skills */}
        {matchResult.missing_skills && matchResult.missing_skills.length > 0 && (
          <div className="mb-4">
            <h3 className="font-medium text-gray-700 mb-1">Missing Skills</h3>
            <div className="flex flex-wrap gap-2">
              {matchResult.missing_skills.map((skill, index) => {
                // Check if we have detailed missing skill info
                const skillObj = matchResult.missing_skills_details &&
                  matchResult.missing_skills_details[index] ?
                  matchResult.missing_skills_details[index] : { name: skill };

                return (
                  <span
                    key={index}
                    className={`${skillObj.required ? 'bg-red-200 text-red-900' : 'bg-red-100 text-red-800'} rounded-full px-3 py-1 text-sm flex items-center backdrop-blur-sm`}
                  >
                    {typeof skill === 'string' ? skill : skillObj.name}
                    {skillObj.required &&
                      <span className="ml-1 text-xs bg-red-400 text-white px-1 rounded">Required</span>
                    }
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Toggle button for details */}
        <button
          className="w-full mt-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md transition-colors focus:outline-none backdrop-blur-sm"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>

        {/* Detailed skill matches */}
        {showDetails && matchResult.skill_matches && matchResult.skill_matches.length > 0 && (
          <div className="mt-4">
            <h3 className="font-medium text-gray-700 mb-2">Skill Match Details</h3>
            <div className="space-y-2">
              {matchResult.skill_matches.map((match, index) => (
                <div key={index} className="p-3 bg-gray-50 bg-opacity-75 backdrop-blur-sm rounded-md">
                  <div className="flex justify-between mb-2">
                    <div>
                      <span className="font-medium">{match.skill_name}</span>
                      {match.required &&
                        <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-1 rounded">Required</span>
                      }
                    </div>
                    <div className="font-medium flex items-center">
                      <span className={`px-2 py-1 rounded ${getMatchColor(match.match_score * 100)} text-white`}>
                        {Math.round(match.match_score * 100)}%
                      </span>
                    </div>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
                    <div
                      className="h-2.5 rounded-full"
                      style={{
                        width: `${Math.round(match.match_score * 100)}%`,
                        backgroundColor: getMatchColor(match.match_score * 100)
                      }}
                    ></div>
                  </div>

                  <div className="flex flex-wrap gap-x-4 text-xs text-gray-600 mt-2">
                    <div>
                      <span className="font-medium">Importance:</span> {Math.round(match.importance * 100)}%
                    </div>

                    {match.proficiency !== undefined && (
                      <div>
                        <span className="font-medium">Proficiency:</span> {Math.round(match.proficiency * 100)}%
                      </div>
                    )}

                    {match.match_quality !== undefined && (
                      <div>
                        <span className="font-medium">Match Quality:</span> {Math.round(match.match_quality * 100)}%
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Match creation date */}
        {matchResult.created_at && (
          <div className="mt-4 text-right text-xs text-gray-400">
            Matched: {new Date(matchResult.created_at).toLocaleString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchResultCard;