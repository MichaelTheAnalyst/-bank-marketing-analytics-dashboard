import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Card from '../components/Common/Card';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import apiService from '../services/api';

export default function ContactOptimization() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getContactOptimization();
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load contact optimization data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Analyzing contact strategies..." />;
  if (error) return <div className="text-red-600 p-6">{error}</div>;
  if (!data) return null;

  // Prepare frequency chart
  const freqData = data.frequency.filter(f => f.campaign <= 10); // Limit to first 10 for clarity
  const frequencyChart = [
    {
      x: freqData.map(f => f.campaign),
      y: freqData.map(f => f.conversion_rate_pct),
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Conversion Rate %',
      line: { color: '#1f77b4', width: 3 },
      marker: { size: 10 }
    }
  ];

  const frequencyBarChart = [
    {
      x: freqData.map(f => f.campaign),
      y: freqData.map(f => f.total_contacts),
      type: 'bar',
      name: 'Number of Customers',
      marker: { color: 'lightblue' }
    }
  ];

  // Prepare month timing chart
  const monthOrder = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
  const monthData = data.timing.by_month.sort((a, b) => 
    monthOrder.indexOf(a.month) - monthOrder.indexOf(b.month)
  );

  const monthChart = [
    {
      x: monthData.map(m => m.month.toUpperCase()),
      y: monthData.map(m => m.total),
      type: 'bar',
      name: 'Total Contacts',
      marker: { color: 'lightblue' },
      yaxis: 'y',
      opacity: 0.6
    },
    {
      x: monthData.map(m => m.month.toUpperCase()),
      y: monthData.map(m => m.conversion_rate_pct),
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Conversion Rate %',
      line: { color: 'red', width: 3 },
      marker: { size: 10 },
      yaxis: 'y2'
    }
  ];

  // Prepare day timing chart
  const dayOrder = ['mon', 'tue', 'wed', 'thu', 'fri'];
  const dayData = data.timing.by_day.sort((a, b) => 
    dayOrder.indexOf(a.day_of_week) - dayOrder.indexOf(b.day_of_week)
  );

  const dayChart = [
    {
      x: dayData.map(d => d.day_of_week.toUpperCase()),
      y: dayData.map(d => d.total),
      type: 'bar',
      name: 'Total Contacts',
      marker: { color: 'lightgreen' },
      yaxis: 'y',
      opacity: 0.6
    },
    {
      x: dayData.map(d => d.day_of_week.toUpperCase()),
      y: dayData.map(d => d.conversion_rate_pct),
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Conversion Rate %',
      line: { color: 'darkgreen', width: 3 },
      marker: { size: 10 },
      yaxis: 'y2'
    }
  ];

  // Prepare channel chart
  const channelConversionChart = [
    {
      x: data.channel.map(c => c.contact),
      y: data.channel.map(c => c.conversion_rate_pct),
      type: 'bar',
      text: data.channel.map(c => `${c.conversion_rate_pct.toFixed(1)}%`),
      textposition: 'auto',
      marker: { color: ['#FF6B6B', '#4ECDC4'] }
    }
  ];

  const channelVolumeChart = [
    {
      labels: data.channel.map(c => c.contact),
      values: data.channel.map(c => c.total),
      type: 'pie',
      marker: { colors: ['#FF6B6B', '#4ECDC4'] }
    }
  ];

  // Prepare previous outcome chart
  const outcomeChart = [
    {
      x: data.previous_outcome.map(o => o.poutcome),
      y: data.previous_outcome.map(o => o.conversion_rate_pct),
      type: 'bar',
      text: data.previous_outcome.map(o => `${o.conversion_rate_pct.toFixed(1)}%`),
      textposition: 'auto',
      marker: {
        color: data.previous_outcome.map(o => o.conversion_rate_pct),
        colorscale: 'RdYlGn',
        showscale: true
      }
    }
  ];

  // Find optimal values
  const optimalFreq = freqData.reduce((max, f) => 
    f.conversion_rate_pct > max.conversion_rate_pct ? f : max, freqData[0]);
  const bestMonth = monthData.reduce((max, m) => 
    m.conversion_rate_pct > max.conversion_rate_pct ? m : max, monthData[0]);
  const bestDay = dayData.reduce((max, d) => 
    d.conversion_rate_pct > max.conversion_rate_pct ? d : max, dayData[0]);
  const bestChannel = data.channel.reduce((max, c) => 
    c.conversion_rate_pct > max.conversion_rate_pct ? c : max, data.channel[0]);

  return (
    <div className="space-y-6 fade-in">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Contact Optimization</h1>
        <p className="mt-2 text-gray-600">
          Optimize campaign effectiveness through frequency, timing, and channel analysis
        </p>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card hover>
          <div className="text-center">
            <div className="text-4xl mb-2">📞</div>
            <h3 className="font-semibold text-gray-900 mb-1">Optimal Frequency</h3>
            <p className="text-3xl font-bold text-primary">{optimalFreq.campaign}</p>
            <p className="text-sm text-gray-600 mt-1">
              {optimalFreq.conversion_rate_pct.toFixed(1)}% conversion
            </p>
          </div>
        </Card>

        <Card hover>
          <div className="text-center">
            <div className="text-4xl mb-2">📅</div>
            <h3 className="font-semibold text-gray-900 mb-1">Best Month</h3>
            <p className="text-3xl font-bold text-primary">{bestMonth.month.toUpperCase()}</p>
            <p className="text-sm text-gray-600 mt-1">
              {bestMonth.conversion_rate_pct.toFixed(1)}% conversion
            </p>
          </div>
        </Card>

        <Card hover>
          <div className="text-center">
            <div className="text-4xl mb-2">📆</div>
            <h3 className="font-semibold text-gray-900 mb-1">Best Day</h3>
            <p className="text-3xl font-bold text-primary">{bestDay.day_of_week.toUpperCase()}</p>
            <p className="text-sm text-gray-600 mt-1">
              {bestDay.conversion_rate_pct.toFixed(1)}% conversion
            </p>
          </div>
        </Card>

        <Card hover>
          <div className="text-center">
            <div className="text-4xl mb-2">📱</div>
            <h3 className="font-semibold text-gray-900 mb-1">Best Channel</h3>
            <p className="text-3xl font-bold text-primary capitalize">{bestChannel.contact}</p>
            <p className="text-sm text-gray-600 mt-1">
              {bestChannel.conversion_rate_pct.toFixed(1)}% conversion
            </p>
          </div>
        </Card>
      </div>

      {/* Contact Frequency Analysis */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Contact Frequency Impact
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Plot
            data={frequencyChart}
            layout={{
              autosize: true,
              height: 300,
              margin: { t: 20, b: 50, l: 50, r: 20 },
              xaxis: { title: 'Number of Contacts' },
              yaxis: { title: 'Conversion Rate (%)' },
              showlegend: false
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
          <Plot
            data={frequencyBarChart}
            layout={{
              autosize: true,
              height: 300,
              margin: { t: 20, b: 50, l: 50, r: 20 },
              xaxis: { title: 'Number of Contacts' },
              yaxis: { title: 'Number of Customers' },
              showlegend: false
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>
      </Card>

      {/* Timing Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Conversion Rate by Month
          </h3>
          <Plot
            data={monthChart}
            layout={{
              autosize: true,
              height: 400,
              xaxis: { title: 'Month' },
              yaxis: { title: 'Total Contacts', side: 'left' },
              yaxis2: { 
                title: 'Conversion Rate (%)', 
                side: 'right', 
                overlaying: 'y' 
              },
              legend: { orientation: 'h', y: -0.2 }
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Conversion Rate by Day of Week
          </h3>
          <Plot
            data={dayChart}
            layout={{
              autosize: true,
              height: 400,
              xaxis: { title: 'Day of Week' },
              yaxis: { title: 'Total Contacts', side: 'left' },
              yaxis2: { 
                title: 'Conversion Rate (%)', 
                side: 'right', 
                overlaying: 'y' 
              },
              legend: { orientation: 'h', y: -0.2 }
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </Card>
      </div>

      {/* Channel Analysis */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Contact Channel Analysis
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Plot
            data={channelConversionChart}
            layout={{
              autosize: true,
              height: 300,
              xaxis: { title: 'Contact Channel' },
              yaxis: { title: 'Conversion Rate (%)' },
              showlegend: false
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
          <Plot
            data={channelVolumeChart}
            layout={{
              autosize: true,
              height: 300,
              showlegend: true,
              legend: { orientation: 'h', y: -0.1 }
            }}
            config={{ responsive: true }}
            style={{ width: '100%' }}
          />
        </div>
      </Card>

      {/* Previous Outcome Impact */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Impact of Previous Campaign Outcome
        </h3>
        <Plot
          data={outcomeChart}
          layout={{
            autosize: true,
            height: 400,
            xaxis: { title: 'Previous Campaign Outcome' },
            yaxis: { title: 'Conversion Rate (%)' },
            showlegend: false
          }}
          config={{ responsive: true }}
          style={{ width: '100%' }}
        />
      </Card>

      {/* Action Items */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">💡 Key Recommendations</h3>
        <div className="space-y-3 text-gray-700">
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p>
              <strong>Optimal Contact Frequency:</strong> Limit campaigns to {optimalFreq.campaign}-3 contacts maximum 
              to avoid customer fatigue while maintaining {optimalFreq.conversion_rate_pct.toFixed(1)}% conversion rate
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p>
              <strong>Best Timing:</strong> Focus campaigns during {bestMonth.month.toUpperCase()} 
              and prioritize {bestDay.day_of_week.toUpperCase()} for initial contacts
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p>
              <strong>Channel Strategy:</strong> Prioritize {bestChannel.contact} as primary channel 
              with {bestChannel.conversion_rate_pct.toFixed(1)}% conversion rate
            </p>
          </div>
          <div className="flex items-start">
            <span className="inline-block w-2 h-2 bg-primary rounded-full mt-2 mr-3"></span>
            <p>
              <strong>Re-engagement:</strong> Create separate strategy for customers with previous successful 
              engagements - they show significantly higher conversion rates
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
