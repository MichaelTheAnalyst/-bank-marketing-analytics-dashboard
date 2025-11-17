/**
 * API Service for communicating with Flask backend
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),

  // Overview
  getOverview: () => api.get('/overview'),
  getAgeDistribution: () => api.get('/overview/age-distribution'),

  // Feature Importance
  getFeatureImportance: () => api.get('/feature-importance'),

  // Predictive Models
  getPredictiveModels: () => api.get('/predictive-models'),

  // Customer Segmentation
  getCustomerSegmentation: (nClusters = 4) => 
    api.get(`/customer-segmentation?n_clusters=${nClusters}`),

  // Contact Optimization
  getContactOptimization: () => api.get('/contact-optimization'),

  // Economic Impact
  getEconomicImpact: () => api.get('/economic-impact'),
};

export default apiService;

