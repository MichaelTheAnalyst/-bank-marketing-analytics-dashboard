import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';

export default function FeatureImportance() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState('aggregated');
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getFeatureImportance();
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load feature importance data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Analyzing feature importance..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  const currentData = data[selectedMethod] || [];
  
  // Prepare chart data
  const features = currentData.map(d => d.feature.replace('_encoded', '').replace(/_/g, ' '));
  const importances = currentData.map(d => d.importance);

  const chartData = [
    {
      y: features,
      x: importances,
      type: 'bar',
      orientation: 'h',
      marker: {
        color: importances,
        colorscale: 'Viridis',
        showscale: true,
      },
    },
  ];

  const insights = [
    {
      title: 'Economic Indicators',
      content: 'Euribor3m and nr.employed are top predictors - macroeconomic conditions significantly influence campaign success.',
      icon: '📊',
    },
    {
      title: 'Previous Campaign Impact',
      content: 'Previous campaign outcome (poutcome) is a strong predictor - past behavior indicates future response.',
      icon: '🔄',
    },
    {
      title: 'Contact Timing',
      content: 'Month of contact matters - seasonal patterns in subscription behavior detected.',
      icon: '📅',
    },
    {
      title: 'Actionable Insight',
      content: 'Focus on economic timing and leverage previous success patterns for better targeting.',
      icon: '💡',
    },
  ];

  return (
    <div className="space-y-6 fade-in">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Feature Importance Analysis</h1>
        <p className="mt-2 text-gray-600">
          Identify key drivers of term deposit subscription across multiple ML algorithms
        </p>
      </div>

      {/* Method Selector */}
      <Card>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Analysis Method</h3>
          <div className="flex space-x-2">
            {['aggregated', 'random_forest', 'gradient_boosting', 'logistic_regression'].map((method) => (
              <button
                key={method}
                onClick={() => setSelectedMethod(method)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedMethod === method
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {method.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* Feature Importance Chart */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Top {currentData.length} Features - {selectedMethod.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </h3>
        <Plot
          data={chartData}
          layout={{
            autosize: true,
            height: 500,
            margin: { t: 20, b: 50, l: 150, r: 50 },
            xaxis: { title: 'Importance Score' },
            yaxis: { title: '', autorange: 'reversed' },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      {/* Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {insights.map((insight, index) => (
          <Card key={index} hover>
            <div className="flex items-start space-x-3">
              <div className="text-4xl">{insight.icon}</div>
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900 mb-2">{insight.title}</h4>
                <p className="text-gray-600 text-sm">{insight.content}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Key Takeaways */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">🔍 Key Takeaways</h3>
        <div className="space-y-3">
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p className="text-gray-700">
              <strong>Economic indicators</strong> (euribor3m, nr.employed) are the strongest predictors - 
              campaign success is highly dependent on macroeconomic conditions
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p className="text-gray-700">
              <strong>Previous campaign outcome</strong> is crucial - customers who responded positively before 
              are more likely to subscribe again
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p className="text-gray-700">
              <strong>Contact timing matters</strong> - month of contact shows seasonal patterns in subscription behavior
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p className="text-gray-700">
              <strong>Customer demographics</strong> (age, job, education) provide secondary but important signals
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}

