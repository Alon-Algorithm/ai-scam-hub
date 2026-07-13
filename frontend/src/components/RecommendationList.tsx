import React from 'react';

interface RecommendationListProps {
  recommendations: string[];
}

export const RecommendationList: React.FC<RecommendationListProps> = ({ recommendations }) => {
  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
      <h4 className="font-semibold text-green-800 mb-2">Recommended Actions:</h4>
      <ul className="space-y-2">
        {recommendations.map((recommendation, idx) => (
          <li key={idx} className="text-green-700 flex items-start">
            <span className="mr-2">✓</span>
            {recommendation}
          </li>
        ))}
      </ul>
    </div>
  );
};