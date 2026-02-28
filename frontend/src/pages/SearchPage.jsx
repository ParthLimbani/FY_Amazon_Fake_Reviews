/**
 * Search Page
 * ===========
 * Landing page with search input and feature highlights.
 */

import { useState } from 'react';
import { Shield, Zap, BarChart3, AlertTriangle, CheckCircle, Eye } from 'lucide-react';
import SearchInput from '../components/SearchInput';
import { analyzeProduct, getDemoAnalysis } from '../services/api';

const SearchPage = ({ onStartAnalysis, onComplete, onError, error }) => {
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Handle URL submission
   */
  const handleSubmit = async (url) => {
    setIsLoading(true);
    onStartAnalysis();
    
    try {
      const result = await analyzeProduct(url);
      onComplete(result);
    } catch (err) {
      onError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Load demo data for testing
   */
  const handleDemoClick = async () => {
    setIsLoading(true);
    onStartAnalysis();
    
    try {
      const result = await getDemoAnalysis();
      onComplete(result);
    } catch (err) {
      onError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      icon: Shield,
      title: 'AI-Powered Detection',
      description: 'Advanced ML algorithms analyze review patterns to identify fake or incentivized reviews.',
    },
    {
      icon: BarChart3,
      title: 'Detailed Analytics',
      description: 'Get comprehensive metrics including adjusted ratings and authenticity grades.',
    },
    {
      icon: Eye,
      title: 'Explainable Results',
      description: 'Understand exactly why each review was flagged with clear, interpretable reasons.',
    },
    {
      icon: Zap,
      title: 'Fast Analysis',
      description: 'Get results in seconds with our optimized processing pipeline.',
    },
  ];

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
          Detect Fake Amazon Reviews
          <span className="text-blue-600"> Instantly</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Don't trust fake reviews. Our AI analyzes Amazon product reviews to help you 
          make informed purchasing decisions.
        </p>

        {/* Search Input */}
        <SearchInput 
          onSubmit={handleSubmit} 
          isLoading={isLoading}
          error={error}
        />

        {/* Demo Link */}
        <div className="mt-4">
          <button
            onClick={handleDemoClick}
            disabled={isLoading}
            className="text-sm text-blue-600 hover:text-blue-800 underline"
          >
            Try with demo data →
          </button>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="max-w-5xl mx-auto mt-20" id="how-it-works">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-12">
          How It Works
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl font-bold text-blue-600">1</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Paste URL</h3>
            <p className="text-gray-600 text-sm">
              Enter any Amazon India product URL to start the analysis
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl font-bold text-blue-600">2</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
            <p className="text-gray-600 text-sm">
              Our ML model analyzes each review for fake patterns and signals
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl font-bold text-blue-600">3</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Get Results</h3>
            <p className="text-gray-600 text-sm">
              View detailed analysis with authenticity scores and explanations
            </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-5xl mx-auto mt-20" id="features">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-12">
          Features
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="flex items-start space-x-4 p-6 bg-white rounded-xl shadow-sm border border-gray-100 card-hover"
            >
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <feature.icon className="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{feature.title}</h3>
                <p className="text-gray-600 text-sm mt-1">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Detection Signals */}
      <div className="max-w-5xl mx-auto mt-20">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-12">
          What We Detect
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <span className="text-gray-700">Excessive positivity without details</span>
          </div>
          <div className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <span className="text-gray-700">Short, generic reviews</span>
          </div>
          <div className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <span className="text-gray-700">Marketing language patterns</span>
          </div>
          <div className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <span className="text-gray-700">Unverified purchase indicators</span>
          </div>
          <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <span className="text-gray-700">Verified purchase validation</span>
          </div>
          <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <span className="text-gray-700">Detailed, specific feedback</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
