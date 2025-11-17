import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';

export default function PredictiveModels() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [selectedModel, setSelectedModel] = useState('Random Forest');
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getPredictiveModels();
      setData(response.data);
      const firstModel = Object.keys(response.data.metrics)[0];
      setSelectedModel(firstModel);
      setError(null);
    } catch (err) {
      setError('Failed to load predictive models data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Training models... This may take a minute..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  // Prepare metrics comparison chart
  const models = Object.keys(data.metrics);
  const metrics = ['accuracy', 'precision', 'recall', 'f1'];
  
  const metricsData = metrics.map(metric => ({
    x: models,
    y: models.map(model => data.metrics[model][metric]),
    name: metric.toUpperCase(),
    type: 'bar',
  }));

  // Prepare ROC curve data
  const rocData = Object.entries(data.roc_curves || {}).map(([model, rocData]) => ({
    x: rocData.fpr,
    y: rocData.tpr,
    name: `${model} (AUC=${rocData.auc.toFixed(3)})`,
    type: 'scatter',
    mode: 'lines',
  }));

  // Add diagonal line
  rocData.push({
    x: [0, 1],
    y: [0, 1],
    name: 'Random Classifier',
    type: 'scatter',
    mode: 'lines',
    line: { dash: 'dash', color: 'gray' },
  });

  // Confusion matrix for selected model
  const cm = data.confusion_matrices[selectedModel];
  const confusionData = [{
    z: cm,
    x: ['Predicted No', 'Predicted Yes'],
    y: ['Actual No', 'Actual Yes'],
    type: 'heatmap',
    colorscale: 'Blues',
    showscale: true,
  }];

  // Best model
  const bestModel = models.reduce((best, model) => 
    data.metrics[model].f1 > data.metrics[best].f1 ? model : best
  , models[0]);

  return (
    <div className="space-y-6 fade-in">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Predictive Models</h1>
        <p className="mt-2 text-gray-600">
          Realistic pre-call prediction models (excluding call duration)
        </p>
      </div>

      {/* Best Model Highlight */}
      <Card>
        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-bold text-gray-900">🏆 Best Performing Model</h3>
              <p className="text-4xl font-bold text-primary mt-2">{bestModel}</p>
              <p className="text-gray-600 mt-2">
                F1-Score: {data.metrics[bestModel].f1.toFixed(3)} | 
                Accuracy: {(data.metrics[bestModel].accuracy * 100).toFixed(1)}%
              </p>
            </div>
            <div className="text-6xl">🎯</div>
          </div>
        </div>
      </Card>

      {/* Metrics Comparison */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Model Performance Comparison
        </h3>
        <Plot
          data={metricsData}
          layout={{
            autosize: true,
            height: 400,
            barmode: 'group',
            xaxis: { title: 'Model' },
            yaxis: { title: 'Score', range: [0, 1] },
            legend: { orientation: 'h', y: 1.1 },
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ROC Curves */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            ROC Curves - Model Comparison
          </h3>
          <Plot
            data={rocData}
            layout={{
              autosize: true,
              height: 400,
              xaxis: { title: 'False Positive Rate' },
              yaxis: { title: 'True Positive Rate' },
              legend: { orientation: 'v', y: 0.5 },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        </Card>

        {/* Confusion Matrix */}
        <Card>
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Confusion Matrix
            </h3>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50"
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
          <Plot
            data={confusionData}
            layout={{
              autosize: true,
              height: 350,
              xaxis: { title: 'Predicted Label' },
              yaxis: { title: 'True Label' },
            }}
            config={{ responsive: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      {/* Detailed Metrics Table */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Detailed Performance Metrics
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Accuracy
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Precision
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Recall
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  F1-Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ROC-AUC
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {models.map(model => (
                <tr key={model} className={model === bestModel ? 'bg-green-50' : ''}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {model} {model === bestModel && '🏆'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {data.metrics[model].accuracy.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {data.metrics[model].precision.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {data.metrics[model].recall.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {data.metrics[model].f1.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {data.metrics[model].roc_auc?.toFixed(4) || 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Insights */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">💡 Model Insights</h3>
        <div className="space-y-3 text-gray-700">
          <p>
            ✅ <strong>Best Model:</strong> {bestModel} achieves an F1-score of {data.metrics[bestModel].f1.toFixed(3)}, 
            balancing precision and recall effectively.
          </p>
          <p>
            📊 <strong>Performance:</strong> Models achieve {(data.metrics[bestModel].accuracy * 100).toFixed(1)}% accuracy, 
            demonstrating strong predictive capability without using call duration.
          </p>
          <p>
            🎯 <strong>Business Impact:</strong> These models can prioritize customer contacts BEFORE calling, 
            enabling efficient resource allocation and improved campaign ROI.
          </p>
          <p>
            🚀 <strong>Deployment Ready:</strong> All features are available pre-call, making these models 
            suitable for real-time lead scoring and prioritization systems.
          </p>
        </div>
      </Card>
    </div>
  );
}

