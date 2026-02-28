/**
 * Product Info Component
 * ======================
 * Displays product information including image, title, and actions.
 */

import { ExternalLink, RefreshCw } from 'lucide-react';

const ProductInfo = ({ product, isDemo = false, onAnalyzeAnother }) => {
  const {
    product_title,
    product_image,
    product_url,
    asin,
    analysis_date,
  } = product;

  // Format analysis date
  const formattedDate = new Date(analysis_date).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Product Image */}
        <div className="flex-shrink-0">
          {product_image ? (
            <img
              src={product_image}
              alt={product_title}
              className="w-32 h-32 object-contain rounded-lg bg-gray-50"
            />
          ) : (
            <div className="w-32 h-32 bg-gray-100 rounded-lg flex items-center justify-center">
              <span className="text-gray-400 text-sm">No Image</span>
            </div>
          )}
        </div>

        {/* Product Details */}
        <div className="flex-grow">
          <h2 className="text-xl font-semibold text-gray-900 line-clamp-2">
            {product_title}
          </h2>
          
          <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-500">
            <span className="flex items-center">
              <span className="font-medium text-gray-700 mr-1">ASIN:</span>
              {asin}
            </span>
            <span className="flex items-center">
              <span className="font-medium text-gray-700 mr-1">Analyzed:</span>
              {formattedDate}
            </span>
          </div>

          {/* Action Buttons */}
          <div className="mt-4 flex flex-wrap gap-3">
            {!isDemo && (
              <a
                href={product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white text-sm font-medium rounded-lg transition-colors"
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                View on Amazon
              </a>
            )}
            <button
              onClick={onAnalyzeAnother}
              className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Analyze Another Product
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductInfo;
