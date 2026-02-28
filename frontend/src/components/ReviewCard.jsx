/**
 * Review Card Component
 * =====================
 * Displays individual review with classification result.
 */

import { CheckCircle, XCircle, Star, BadgeCheck } from 'lucide-react';

const ReviewCard = ({ review }) => {
  const {
    reviewer_name,
    rating,
    title,
    text,
    date,
    verified_purchase,
    label,
    confidence,
    reasons,
  } = review;

  const isFake = label === 'fake';
  const confidencePercent = Math.round(confidence * 100);

  // Generate star rating display
  const stars = Array(5).fill(0).map((_, i) => (
    <Star
      key={i}
      className={`h-4 w-4 ${i < rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
    />
  ));

  return (
    <div className={`bg-white rounded-xl p-5 shadow-sm border-2 transition-all ${
      isFake ? 'border-red-200 bg-red-50/30' : 'border-green-200 bg-green-50/30'
    }`}>
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          {/* Classification badge */}
          <div className={`p-2 rounded-full ${isFake ? 'bg-red-100' : 'bg-green-100'}`}>
            {isFake ? (
              <XCircle className="h-5 w-5 text-red-600" />
            ) : (
              <CheckCircle className="h-5 w-5 text-green-600" />
            )}
          </div>
          
          <div>
            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-900">{reviewer_name}</span>
              {verified_purchase && (
                <span className="inline-flex items-center text-xs text-green-700 bg-green-100 px-2 py-0.5 rounded-full">
                  <BadgeCheck className="h-3 w-3 mr-1" />
                  Verified
                </span>
              )}
            </div>
            <div className="flex items-center gap-2 mt-1">
              <div className="flex">{stars}</div>
              <span className="text-sm text-gray-500">{date}</span>
            </div>
          </div>
        </div>

        {/* Confidence score */}
        <div className={`text-right ${isFake ? 'text-red-600' : 'text-green-600'}`}>
          <span className="text-sm font-medium">
            {isFake ? 'Likely Fake' : 'Likely Genuine'}
          </span>
          <div className="text-xs text-gray-500">
            {confidencePercent}% confidence
          </div>
        </div>
      </div>

      {/* Review content */}
      <div className="mt-4">
        <h4 className="font-medium text-gray-900">{title}</h4>
        <p className="mt-2 text-gray-600 text-sm leading-relaxed">
          {text}
        </p>
      </div>

      {/* Reasons */}
      {reasons && reasons.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <h5 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">
            {isFake ? 'Suspicious Patterns Detected' : 'Genuine Indicators'}
          </h5>
          <div className="flex flex-wrap gap-2">
            {reasons.map((reason, index) => (
              <span
                key={index}
                className={`text-xs px-2 py-1 rounded-full ${
                  isFake ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                }`}
              >
                {reason}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReviewCard;
