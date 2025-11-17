import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import Overview from './pages/Overview';
import FeatureImportance from './pages/FeatureImportance';
import PredictiveModels from './pages/PredictiveModels';
import CustomerSegmentation from './pages/CustomerSegmentation';
import ContactOptimization from './pages/ContactOptimization';
import EconomicImpact from './pages/EconomicImpact';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gradient-to-br from-neutral-50 via-white to-primary-50">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 flex flex-col ml-64">
          {/* Header */}
          <Header />

          {/* Content Area */}
          <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
            <div className="max-w-[1600px] mx-auto">
              <Routes>
                <Route path="/" element={<Overview />} />
                <Route path="/feature-importance" element={<FeatureImportance />} />
                <Route path="/predictive-models" element={<PredictiveModels />} />
                <Route path="/segmentation" element={<CustomerSegmentation />} />
                <Route path="/contact-optimization" element={<ContactOptimization />} />
                <Route path="/economic-impact" element={<EconomicImpact />} />
              </Routes>
            </div>
          </main>

          {/* Footer */}
          <footer className="bg-white/80 backdrop-blur-md border-t border-neutral-200/50 py-8 px-8">
            <div className="max-w-[1600px] mx-auto">
              <div className="text-center space-y-4">
                <div>
                  <p className="text-xl font-bold text-gradient font-display">Masood Nazari</p>
                  <p className="text-sm text-neutral-600 mt-1">Data Science | AI | Clinical Research</p>
                </div>
                <div className="flex items-center justify-center gap-8 flex-wrap text-sm">
                  <a 
                    href="mailto:M.Nazari@soton.ac.uk" 
                    className="text-neutral-600 hover:text-primary-600 transition-all duration-200 flex items-center gap-2 group"
                  >
                    <span className="w-8 h-8 bg-primary-50 group-hover:bg-primary-100 rounded-lg flex items-center justify-center transition-colors">✉️</span>
                    <span className="group-hover:translate-x-1 transition-transform">M.Nazari@soton.ac.uk</span>
                  </a>
                  <a 
                    href="https://michaeltheanalyst.github.io/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-neutral-600 hover:text-primary-600 transition-all duration-200 flex items-center gap-2 group"
                  >
                    <span className="w-8 h-8 bg-primary-50 group-hover:bg-primary-100 rounded-lg flex items-center justify-center transition-colors">🌐</span>
                    <span className="group-hover:translate-x-1 transition-transform">Portfolio</span>
                  </a>
                  <a 
                    href="https://www.linkedin.com/in/masood-nazari/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-neutral-600 hover:text-primary-600 transition-all duration-200 flex items-center gap-2 group"
                  >
                    <span className="w-8 h-8 bg-primary-50 group-hover:bg-primary-100 rounded-lg flex items-center justify-center transition-colors">💼</span>
                    <span className="group-hover:translate-x-1 transition-transform">LinkedIn</span>
                  </a>
                  <a 
                    href="https://github.com/michaeltheanalyst" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-neutral-600 hover:text-primary-600 transition-all duration-200 flex items-center gap-2 group"
                  >
                    <span className="w-8 h-8 bg-primary-50 group-hover:bg-primary-100 rounded-lg flex items-center justify-center transition-colors">🔗</span>
                    <span className="group-hover:translate-x-1 transition-transform">GitHub</span>
                  </a>
                </div>
                <div className="pt-4 border-t border-neutral-200/50">
                  <p className="text-xs text-neutral-400">
                    © 2025 Bank Marketing Analytics | Built with React & Flask | <span className="text-primary-600">Made with ❤️</span>
                  </p>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </Router>
  );
}

export default App;

