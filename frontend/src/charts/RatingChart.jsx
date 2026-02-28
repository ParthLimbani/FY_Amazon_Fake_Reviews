/**
 * Rating Distribution Chart Component
 * ====================================
 * Displays rating distribution for genuine vs fake reviews.
 */

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const RatingChart = ({ reviews }) => {
  // Calculate rating distribution
  const calculateDistribution = () => {
    const distribution = {
      1: { rating: '1 Star', genuine: 0, fake: 0 },
      2: { rating: '2 Stars', genuine: 0, fake: 0 },
      3: { rating: '3 Stars', genuine: 0, fake: 0 },
      4: { rating: '4 Stars', genuine: 0, fake: 0 },
      5: { rating: '5 Stars', genuine: 0, fake: 0 },
    };

    reviews.forEach((review) => {
      const rating = Math.round(review.rating);
      const clampedRating = Math.max(1, Math.min(5, rating));
      
      if (review.label === 'fake') {
        distribution[clampedRating].fake += 1;
      } else {
        distribution[clampedRating].genuine += 1;
      }
    });

    return Object.values(distribution);
  };

  const data = calculateDistribution();

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Rating Distribution
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="rating" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Bar
              dataKey="genuine"
              name="Genuine Reviews"
              fill="#22c55e"
              radius={[4, 4, 0, 0]}
            />
            <Bar
              dataKey="fake"
              name="Fake Reviews"
              fill="#ef4444"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RatingChart;
