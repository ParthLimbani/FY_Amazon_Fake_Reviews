/**
 * Footer Component
 * ================
 * Application footer with project info and links.
 */

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white font-semibold mb-4">About</h3>
            <p className="text-sm">
              FakeReviewDetector uses machine learning and NLP to analyze 
              Amazon product reviews and identify potential fake or incentivized reviews.
            </p>
          </div>
          
          {/* Tech Stack */}
          <div>
            <h3 className="text-white font-semibold mb-4">Tech Stack</h3>
            <ul className="text-sm space-y-2">
              <li>React + Vite + Tailwind CSS</li>
              <li>Python + FastAPI</li>
              <li>scikit-learn + NLP</li>
              <li>Canopy API</li>
            </ul>
          </div>
          
          {/* Disclaimer */}
          <div>
            <h3 className="text-white font-semibold mb-4">Disclaimer</h3>
            <p className="text-sm">
              This tool provides analysis based on patterns and heuristics. 
              Results should be used as guidance, not definitive judgments.
              For educational purposes only.
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-sm">
          <p>© 2025 Fake Review Detector - Final Year Project</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
