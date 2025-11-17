import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';

export default function CustomerSegmentation() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [nClusters, setNClusters] = useState(4);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nClusters]);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getCustomerSegmentation(nClusters);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load segmentation data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Performing customer segmentation..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  // Prepare PCA visualization
  const pcaData = [{
    x: data.pca_data.pc1,
    y: data.pca_data.pc2,
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 5,
      color: data.pca_data.segment,
      colorscale: 'Viridis',
      showscale: true,
    },
    text: data.pca_data.subscribed,
  }];

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Customer Segmentation</h1>
        <p className="mt-2 text-gray-600">
          Identify distinct customer segments for targeted marketing strategies
        </p>
      </div>

      {/* Cluster Selector */}
      <Card>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Number of Segments</h3>
          <div className="flex items-center space-x-4">
            <input
              type="range"
              min="3"
              max="6"
              value={nClusters}
              onChange={(e) => setNClusters(parseInt(e.target.value))}
              className="w-32"
            />
            <span className="text-2xl font-bold text-primary">{nClusters}</span>
          </div>
        </div>
      </Card>

      {/* PCA Visualization */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Customer Segments Visualization (PCA)
        </h3>
        <Plot
          data={pcaData}
          layout={{
            autosize: true,
            height: 500,
            xaxis: { title: `PC1 (${(data.pca_data.explained_variance[0] * 100).toFixed(1)}%)` },
            yaxis: { title: `PC2 (${(data.pca_data.explained_variance[1] * 100).toFixed(1)}%)` },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      {/* Segment Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {data.segments.map((segment, idx) => (
          <Card key={idx} hover>
            <h3 className="text-xl font-bold text-primary mb-3">{segment.Segment}</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Size:</span>
                <span className="font-semibold">{segment['Size %']}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Conversion Rate:</span>
                <span className="font-semibold text-green-600">{segment['Conversion Rate']}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Age:</span>
                <span className="font-semibold">{segment['Avg Age']}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Top Job:</span>
                <span className="font-semibold">{segment['Top Job']}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Top Education:</span>
                <span className="font-semibold">{segment['Top Education']}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

