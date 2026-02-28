/**
 * Metric Card Component
 * =====================
 * Displays a single metric with icon, value, and label.
 */

const MetricCard = ({ icon: Icon, label, value, subValue, colorClass = 'text-gray-900' }) => {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{label}</p>
          <p className={`text-3xl font-bold mt-1 ${colorClass}`}>
            {value}
          </p>
          {subValue && (
            <p className="text-sm text-gray-400 mt-1">{subValue}</p>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-gray-50 rounded-lg">
            <Icon className="h-6 w-6 text-gray-600" />
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
