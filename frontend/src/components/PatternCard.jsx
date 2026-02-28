/**
 * Pattern Card Component
 * ======================
 * Displays a detected pattern in fake reviews.
 */

import { AlertTriangle } from 'lucide-react';

const PatternCard = ({ pattern }) => {
  const { pattern_type, description, frequency } = pattern;

  // Icon mapping for pattern types
  const getPatternIcon = (type) => {
    return AlertTriangle;
  };

  const Icon = getPatternIcon(pattern_type);

  return (
    <div className="flex items-start space-x-3 p-4 bg-amber-50 rounded-lg border border-amber-100">
      <div className="flex-shrink-0">
        <Icon className="h-5 w-5 text-amber-600" />
      </div>
      <div className="flex-grow">
        <div className="flex items-center justify-between">
          <h4 className="font-medium text-gray-900 capitalize">
            {pattern_type.replace(/_/g, ' ')}
          </h4>
          <span className="text-sm text-amber-700 font-medium">
            {frequency} reviews
          </span>
        </div>
        <p className="text-sm text-gray-600 mt-1">{description}</p>
      </div>
    </div>
  );
};

export default PatternCard;
