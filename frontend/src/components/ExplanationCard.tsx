import React from 'react';

interface ExplanationCardProps {
  explanations: string[];
}

export const ExplanationCard: React.FC<ExplanationCardProps> = ({ explanations }) => {
  if (!explanations || explanations.length === 0) {
    return null;
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <h4 className="font-semibold text-blue-800 mb-2">Why This Was Detected:</h4>
      <ul className="space-y-2">
        {explanations.map((explanation, idx) => (
          <li key={idx} className="text-blue-700 flex items-start">
            <span className="mr-2">•</span>
            {explanation}
          </li>
        ))}
      </ul>
    </div>
  );
};