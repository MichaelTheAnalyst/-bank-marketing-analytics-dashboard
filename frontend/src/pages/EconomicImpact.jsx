import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';

export default function EconomicImpact() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getEconomicImpact();
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load economic impact data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Analyzing economic impact..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  // Prepare correlation chart
  const corrData = [{
    y: data.correlations.map(d => d.Indicator),
    x: data.correlations.map(d => d.Correlation),
    type: 'bar',
    orientation: 'h',
    marker: {
      color: data.correlations.map(d => d.Correlation < 0 ? 'red' : 'green'),
    },
  }];

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Economic Impact Analysis</h1>
        <p className="mt-2 text-gray-600">
          Understand how macroeconomic factors influence campaign success
        </p>
      </div>

      {/* Correlations Chart */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Economic Indicators Correlation with Conversion
        </h3>
        <Plot
          data={corrData}
          layout={{
            autosize: true,
            height: 400,
            xaxis: { title: 'Correlation Coefficient' },
            yaxis: { title: '' },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      {/* Correlation Details Table */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Detailed Correlation Analysis
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Indicator
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Correlation
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  P-Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Significant
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.correlations.map((row, idx) => (
                <tr key={idx}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {row.Indicator}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {row.Correlation.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {row['P-Value'].toFixed(6)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      row.Significant === 'Yes' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {row.Significant}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Economic Conditions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {data.conditions.map((cond, idx) => (
          <Card key={idx} hover>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{cond.condition}</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Customers:</span>
                <span className="font-semibold">{cond.total.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Conversion Rate:</span>
                <span className="font-semibold text-green-600">{cond.conversion_rate_pct.toFixed(2)}%</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

