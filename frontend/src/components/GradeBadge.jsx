/**
 * Grade Badge Component
 * =====================
 * Displays the authenticity grade with appropriate styling.
 * Grades: A (best) to F (worst)
 */

const GradeBadge = ({ grade, size = 'large' }) => {
  // Grade color mapping
  const gradeColors = {
    'A': 'bg-green-500',
    'B': 'bg-lime-500',
    'C': 'bg-yellow-500',
    'D': 'bg-orange-500',
    'F': 'bg-red-500',
    'N/A': 'bg-gray-400',
  };

  const sizeClasses = {
    'small': 'w-10 h-10 text-xl',
    'medium': 'w-16 h-16 text-3xl',
    'large': 'w-24 h-24 text-5xl',
  };

  const colorClass = gradeColors[grade] || gradeColors['N/A'];
  const sizeClass = sizeClasses[size] || sizeClasses['large'];

  return (
    <div 
      className={`${colorClass} ${sizeClass} rounded-full flex items-center justify-center text-white font-bold shadow-lg`}
    >
      {grade}
    </div>
  );
};

export default GradeBadge;
