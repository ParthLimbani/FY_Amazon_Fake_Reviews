/**
 * Loading Page
 * ============
 * Displayed while analysis is in progress.
 */

import { Loader2, Search, Brain, BarChart } from 'lucide-react';

const LoadingPage = () => {
  const steps = [
    { icon: Search, label: 'Fetching reviews from Amazon', status: 'active' },
    { icon: Brain, label: 'Running ML classification', status: 'pending' },
    { icon: BarChart, label: 'Generating insights', status: 'pending' },
  ];

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center py-12 px-4">
      {/* Main loading indicator */}
      <div className="relative">
        <div className="w-24 h-24 border-4 border-blue-200 rounded-full animate-spin-slow">
          <div className="absolute top-0 left-1/2 w-4 h-4 bg-blue-600 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
        </div>
      </div>

      {/* Loading text */}
      <h2 className="mt-8 text-2xl font-semibold text-gray-900">
        Analyzing Reviews...
      </h2>
      <p className="mt-2 text-gray-600">
        This may take 30-60 seconds depending on the number of reviews
      </p>

      {/* Progress steps */}
      <div className="mt-10 space-y-4">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`flex items-center space-x-3 ${
              step.status === 'active' ? 'text-blue-600' : 'text-gray-400'
            }`}
          >
            <step.icon className={`h-5 w-5 ${step.status === 'active' ? 'animate-pulse' : ''}`} />
            <span className={step.status === 'active' ? 'font-medium' : ''}>
              {step.label}
            </span>
            {step.status === 'active' && (
              <span className="ml-2 text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                In Progress
              </span>
            )}
          </div>
        ))}
      </div>

      {/* Tips */}
      <div className="mt-12 max-w-md text-center">
        <p className="text-sm text-gray-500">
          💡 <strong>Tip:</strong> While you wait, the AI is analyzing text patterns,
          sentiment, and metadata signals to identify potentially fake reviews.
        </p>
      </div>
    </div>
  );
};

export default LoadingPage;
