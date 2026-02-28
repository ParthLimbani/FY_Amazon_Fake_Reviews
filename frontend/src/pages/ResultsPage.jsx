/**
 * Results Page
 * ============
 * Displays complete analysis results in a dashboard layout.
 * Shows product info, metrics, charts, and individual reviews.
 */

import { useState } from 'react';
import {
  FileText,
  AlertTriangle,
  Star,
  TrendingDown,
  Users,
  Filter,
} from 'lucide-react';

import ProductInfo from '../components/ProductInfo';
import GradeBadge from '../components/GradeBadge';
import MetricCard from '../components/MetricCard';
import SummaryCard from '../components/SummaryCard';
import PatternCard from '../components/PatternCard';
import ReviewCard from '../components/ReviewCard';
import RatingChart from '../charts/RatingChart';
import FakeGenuineChart from '../charts/FakeGenuineChart';

const ResultsPage = ({ result, onAnalyzeAnother }) => {
  const [reviewFilter, setReviewFilter] = useState('all'); // 'all', 'fake', 'genuine'
  
  const {
    asin,
    product_title,
    product_image,
    product_url,
    analysis_date,
    metrics,
    patterns,
    summary,
    reviews,
    is_demo_data = false,
  } = result;

  // Filter reviews based on selection
  const filteredReviews = reviews.filter((review) => {
    if (reviewFilter === 'all') return true;
    return review.label === reviewFilter;
  });

  // Get color class based on fake percentage
  const getFakePercentageColor = (percentage) => {
    if (percentage < 15) return 'text-green-600';
    if (percentage < 30) return 'text-yellow-600';
    if (percentage < 50) return 'text-orange-600';
    return 'text-red-600';
  };

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Demo Data Warning */}
        {is_demo_data && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-yellow-800">Demo Data Notice</h3>
                <p className="text-sm text-yellow-700 mt-1">
                  Canopy API key not configured. Currently showing demo data. 
                  <a 
                    href="https://canopyapi.co" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="underline ml-1"
                  >
                    Get your API key
                  </a> to analyze real Amazon reviews.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Product Info */}
        <ProductInfo
          product={{
            product_title,
            product_image,
            product_url,
            asin,
            analysis_date,
          }}
          isDemo={is_demo_data}
          onAnalyzeAnother={onAnalyzeAnother}
        />

        {/* Main Metrics Grid */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Authenticity Grade */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col items-center justify-center">
            <p className="text-sm font-medium text-gray-500 mb-4">Authenticity Grade</p>
            <GradeBadge grade={metrics.authenticity_grade} size="large" />
            <p className="text-sm text-gray-600 mt-4 text-center">
              {metrics.grade_description}
            </p>
          </div>

          {/* Fake Percentage */}
          <MetricCard
            icon={AlertTriangle}
            label="Fake Reviews"
            value={`${metrics.fake_percentage}%`}
            subValue={`${metrics.fake_count} of ${metrics.total_reviews} reviews`}
            colorClass={getFakePercentageColor(metrics.fake_percentage)}
          />

          {/* Original Rating */}
          <MetricCard
            icon={Star}
            label="Original Rating"
            value={`${metrics.original_rating} ★`}
            subValue="Based on all reviews"
          />

          {/* Adjusted Rating */}
          <MetricCard
            icon={TrendingDown}
            label="Adjusted Rating"
            value={`${metrics.adjusted_rating} ★`}
            subValue={`${metrics.rating_difference > 0 ? '-' : ''}${Math.abs(metrics.rating_difference).toFixed(1)} difference`}
            colorClass={metrics.rating_difference > 0.5 ? 'text-orange-600' : 'text-gray-900'}
          />
        </div>

        {/* Charts and Summary Row */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Pie Chart */}
          <FakeGenuineChart
            fakeCount={metrics.fake_count}
            genuineCount={metrics.genuine_count}
          />

          {/* Bar Chart */}
          <RatingChart reviews={reviews} />

          {/* Summary */}
          <SummaryCard summary={summary} />
        </div>

        {/* Patterns Section */}
        {patterns && patterns.length > 0 && (
          <div className="mt-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <AlertTriangle className="h-5 w-5 text-amber-600 mr-2" />
              Detected Patterns
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {patterns.map((pattern, index) => (
                <PatternCard key={index} pattern={pattern} />
              ))}
            </div>
          </div>
        )}

        {/* Reviews Section */}
        <div className="mt-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Users className="h-5 w-5 text-gray-600 mr-2" />
              Individual Reviews ({filteredReviews.length})
            </h3>
            
            {/* Filter buttons */}
            <div className="flex items-center space-x-2 mt-4 sm:mt-0">
              <Filter className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-500">Filter:</span>
              <div className="flex rounded-lg border border-gray-200 overflow-hidden">
                <button
                  onClick={() => setReviewFilter('all')}
                  className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                    reviewFilter === 'all'
                      ? 'bg-gray-900 text-white'
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setReviewFilter('fake')}
                  className={`px-3 py-1.5 text-sm font-medium transition-colors border-l border-gray-200 ${
                    reviewFilter === 'fake'
                      ? 'bg-red-600 text-white'
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  Fake ({metrics.fake_count})
                </button>
                <button
                  onClick={() => setReviewFilter('genuine')}
                  className={`px-3 py-1.5 text-sm font-medium transition-colors border-l border-gray-200 ${
                    reviewFilter === 'genuine'
                      ? 'bg-green-600 text-white'
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  Genuine ({metrics.genuine_count})
                </button>
              </div>
            </div>
          </div>

          {/* Reviews List */}
          <div className="space-y-4">
            {filteredReviews.slice(0, 20).map((review, index) => (
              <ReviewCard key={review.review_id || index} review={review} />
            ))}
            
            {filteredReviews.length > 20 && (
              <div className="text-center py-4">
                <p className="text-gray-500">
                  Showing 20 of {filteredReviews.length} reviews
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
