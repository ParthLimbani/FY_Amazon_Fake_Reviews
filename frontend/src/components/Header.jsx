/**
 * Header Component
 * ================
 * Application header with logo and navigation.
 */

import { Shield } from 'lucide-react';

const Header = ({ onLogoClick }) => {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <button 
            onClick={onLogoClick}
            className="flex items-center space-x-2 hover:opacity-80 transition-opacity"
          >
            <Shield className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">
              FakeReview<span className="text-blue-600">Detector</span>
            </span>
          </button>
          
          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <a 
              href="#how-it-works" 
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              How it Works
            </a>
            <a 
              href="#features" 
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Features
            </a>
            <a 
              href="https://github.com/ParthLimbani/FY_Amazon_Fake_Reviews" 
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              GitHub
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
