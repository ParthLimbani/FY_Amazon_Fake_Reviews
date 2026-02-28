/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for grades
        'grade-a': '#22c55e', // Green
        'grade-b': '#84cc16', // Lime
        'grade-c': '#eab308', // Yellow
        'grade-d': '#f97316', // Orange
        'grade-f': '#ef4444', // Red
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 2s linear infinite',
      }
    },
  },
  plugins: [],
}
