import React from 'react';

interface RiskBadgeProps {
  level: string;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level }) => {
  const getBadgeStyles = () => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <span className={`px-4 py-2 rounded-full text-sm font-semibold border ${getBadgeStyles()}`}>
      {level} Risk
    </span>
  );
};