/**
 * Summary Card Component
 * ======================
 * Displays the analysis summary with markdown-like formatting.
 */

import { FileText } from 'lucide-react';

const SummaryCard = ({ summary }) => {
  // Parse the summary to handle basic markdown formatting
  const formatSummary = (text) => {
    if (!text) return '';
    
    // Split by newlines
    const lines = text.split('\n');
    
    return lines.map((line, index) => {
      // Handle headers (** bold **)
      if (line.startsWith('**') && line.endsWith('**')) {
        const content = line.replace(/\*\*/g, '');
        return (
          <h4 key={index} className="font-semibold text-gray-900 mt-4 mb-2">
            {content}
          </h4>
        );
      }
      
      // Handle list items
      if (line.startsWith('- ')) {
        const content = line.substring(2);
        // Handle bold within list items
        const formattedContent = content.split(/\*\*(.*?)\*\*/).map((part, i) => 
          i % 2 === 1 ? <strong key={i}>{part}</strong> : part
        );
        return (
          <li key={index} className="ml-4 text-gray-600">
            {formattedContent}
          </li>
        );
      }
      
      // Handle regular paragraphs
      if (line.trim()) {
        // Handle bold within paragraphs
        const formattedContent = line.split(/\*\*(.*?)\*\*/).map((part, i) => 
          i % 2 === 1 ? <strong key={i}>{part}</strong> : part
        );
        return (
          <p key={index} className="text-gray-700 mb-2">
            {formattedContent}
          </p>
        );
      }
      
      return null;
    });
  };

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-gray-900">Analysis Summary</h3>
      </div>
      
      <div className="prose prose-sm max-w-none">
        {formatSummary(summary)}
      </div>
    </div>
  );
};

export default SummaryCard;
