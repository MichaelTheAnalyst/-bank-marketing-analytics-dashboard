import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { MetricCard } from '../components/Common/Card';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';
import {
  UsersIcon,
  CheckCircleIcon,
  ChartBarIcon,
  PhoneIcon,
  CalendarIcon,
} from '@heroicons/react/24/outline';

export default function Overview() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getOverview();
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load overview data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading overview data..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  // Prepare chart data
  const targetData = [
    {
      labels: Object.keys(data.target_distribution),
      values: Object.values(data.target_distribution),
      type: 'pie',
      hole: 0.4,
      marker: {
        colors: ['#FF6B6B', '#4ECDC4'],
      },
    },
  ];

  const jobData = [
    {
      y: Object.keys(data.job_distribution),
      x: Object.values(data.job_distribution),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: '#1f77b4',
      },
    },
  ];

  const educationData = [
    {
      labels: Object.keys(data.education_distribution),
      values: Object.values(data.education_distribution),
      type: 'pie',
      marker: {
        colors: ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3'],
      },
    },
  ];

  return (
    <div className="space-y-6 fade-in">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dataset Overview</h1>
        <p className="mt-2 text-gray-600">
          Comprehensive statistics and visualizations of the bank marketing campaign data
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <MetricCard
          title="Total Customers"
          value={data.total_customers.toLocaleString()}
          icon={UsersIcon}
          color="primary"
        />
        <MetricCard
          title="Conversions"
          value={data.conversions.toLocaleString()}
          icon={CheckCircleIcon}
          color="success"
        />
        <MetricCard
          title="Conversion Rate"
          value={`${data.conversion_rate.toFixed(2)}%`}
          icon={ChartBarIcon}
          color="info"
        />
        <MetricCard
          title="Avg Contacts"
          value={data.avg_contacts.toFixed(1)}
          icon={PhoneIcon}
          color="warning"
        />
        <MetricCard
          title="Campaign Months"
          value={data.unique_months}
          icon={CalendarIcon}
          color="danger"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Target Distribution */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Target Variable Distribution
          </h3>
          <Plot
            data={targetData}
            layout={{
              autosize: true,
              height: 350,
              margin: { t: 0, b: 0, l: 0, r: 0 },
              showlegend: true,
              legend: { orientation: 'h', y: -0.1 },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        </Card>

        {/* Education Distribution */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Education Level Distribution
          </h3>
          <Plot
            data={educationData}
            layout={{
              autosize: true,
              height: 350,
              margin: { t: 0, b: 0, l: 0, r: 0 },
              showlegend: true,
              legend: { orientation: 'h', y: -0.1 },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      {/* Job Distribution */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Top 10 Job Types
        </h3>
        <Plot
          data={jobData}
          layout={{
            autosize: true,
            height: 400,
            margin: { t: 20, b: 50, l: 150, r: 20 },
            xaxis: { title: 'Number of Customers' },
            yaxis: { title: '' },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Age Statistics</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Minimum:</span>
              <span className="font-semibold">{data.age_stats.min} years</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Maximum:</span>
              <span className="font-semibold">{data.age_stats.max} years</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Average:</span>
              <span className="font-semibold">{data.age_stats.mean.toFixed(1)} years</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Median:</span>
              <span className="font-semibold">{data.age_stats.median} years</span>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Contact Methods</h3>
          <div className="space-y-2">
            {Object.entries(data.contact_distribution).map(([method, count]) => (
              <div key={method} className="flex justify-between">
                <span className="text-gray-600 capitalize">{method}:</span>
                <span className="font-semibold">{count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Marital Status</h3>
          <div className="space-y-2">
            {Object.entries(data.marital_distribution).map(([status, count]) => (
              <div key={status} className="flex justify-between">
                <span className="text-gray-600 capitalize">{status}:</span>
                <span className="font-semibold">{count.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

