/**
 * Search Input Component
 * ======================
 * Main search input for entering Amazon product URLs.
 */

import { useState } from 'react';
import { Search, AlertCircle } from 'lucide-react';

const SearchInput = ({ onSubmit, isLoading, error }) => {
  const [url, setUrl] = useState('');
  const [validationError, setValidationError] = useState('');

  /**
   * Validate Amazon URL format
   */
  const validateUrl = (inputUrl) => {
    if (!inputUrl.trim()) {
      return 'Please enter an Amazon product URL';
    }
    
    // Check if it looks like an Amazon URL
    const amazonPattern = /amazon\.(in|com|co\.uk|de|fr|es|it|ca|com\.au)/i;
    const asinPattern = /\/dp\/[A-Z0-9]{10}|\/gp\/product\/[A-Z0-9]{10}/i;
    
    if (!amazonPattern.test(inputUrl) && !asinPattern.test(inputUrl)) {
      // Check if it's just an ASIN
      if (/^[A-Z0-9]{10}$/i.test(inputUrl.trim())) {
        return null; // Valid ASIN
      }
      return 'Please enter a valid Amazon product URL (e.g., amazon.in/dp/XXXXXXXXXX)';
    }
    
    return null;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const error = validateUrl(url);
    if (error) {
      setValidationError(error);
      return;
    }
    
    setValidationError('');
    onSubmit(url);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        
        <input
          type="text"
          value={url}
          onChange={(e) => {
            setUrl(e.target.value);
            setValidationError('');
          }}
          placeholder="Paste Amazon product URL here... (e.g., https://amazon.in/dp/B08N5WRWNW)"
          className={`w-full pl-12 pr-4 py-4 text-lg border-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
            validationError || error
              ? 'border-red-300 bg-red-50'
              : 'border-gray-200 hover:border-gray-300'
          }`}
          disabled={isLoading}
        />
        
        <button
          type="submit"
          disabled={isLoading}
          className="absolute inset-y-2 right-2 px-6 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </span>
          ) : (
            'Analyze'
          )}
        </button>
      </div>
      
      {/* Error messages */}
      {(validationError || error) && (
        <div className="mt-3 flex items-center text-red-600">
          <AlertCircle className="h-5 w-5 mr-2" />
          <span>{validationError || error}</span>
        </div>
      )}
    </form>
  );
};

export default SearchInput;
