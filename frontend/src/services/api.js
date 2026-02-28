/**
 * API Service
 * ===========
 * Centralized API communication layer for the frontend.
 * Handles all HTTP requests to the backend.
 */

import axios from 'axios';

// Base URL for API requests
// In development, Vite proxy handles /api routing to backend
const API_BASE_URL = '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minute timeout for analysis (API can take 2-3 mins)
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze a product URL for fake reviews
 * @param {string} url - Amazon product URL
 * @returns {Promise<Object>} Analysis result
 */
export const analyzeProduct = async (url) => {
  try {
    const response = await apiClient.post('/analyze', { url });
    return response.data;
  } catch (error) {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || 'Analysis failed';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response
      throw new Error('Unable to reach the server. Please check your connection.');
    } else {
      // Error setting up request
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Get demo analysis data for testing
 * @returns {Promise<Object>} Demo analysis result
 */
export const getDemoAnalysis = async () => {
  try {
    const response = await apiClient.get('/demo');
    return response.data;
  } catch (error) {
    throw new Error('Failed to load demo data');
  }
};

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'unhealthy' };
  }
};

export default {
  analyzeProduct,
  getDemoAnalysis,
  checkHealth,
};
