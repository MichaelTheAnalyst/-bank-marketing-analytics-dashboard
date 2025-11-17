import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HomeIcon,
  ChartBarIcon,
  CpuChipIcon,
  UserGroupIcon,
  PhoneIcon,
  CurrencyDollarIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Overview', href: '/', icon: HomeIcon, badge: null },
  { name: 'Feature Importance', href: '/feature-importance', icon: ChartBarIcon, badge: null },
  { name: 'Predictive Models', href: '/predictive-models', icon: CpuChipIcon, badge: 'AI' },
  { name: 'Customer Segmentation', href: '/segmentation', icon: UserGroupIcon, badge: null },
  { name: 'Contact Optimization', href: '/contact-optimization', icon: PhoneIcon, badge: null },
  { name: 'Economic Impact', href: '/economic-impact', icon: CurrencyDollarIcon, badge: null },
];

export default function Sidebar() {
  return (
    <div className="flex flex-col w-64 bg-gradient-to-b from-neutral-900 via-neutral-800 to-neutral-900 h-screen fixed shadow-strong">
      {/* Logo */}
      <div className="flex items-center justify-center h-20 px-4 border-b border-neutral-700/50 bg-gradient-to-r from-primary-900/20 to-transparent">
        <div className="relative">
          <img 
            src="https://img.icons8.com/fluency/96/bank-building.png" 
            alt="Bank Logo" 
            className="w-12 h-12 mr-3 drop-shadow-lg"
          />
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-success-500 rounded-full animate-pulse"></div>
        </div>
        <div>
          <h1 className="text-xl font-bold text-white font-display">Bank Analytics</h1>
          <p className="text-xs text-neutral-400">Intelligence Platform</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto custom-scrollbar">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `group flex items-center justify-between px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg shadow-primary-900/50'
                  : 'text-neutral-300 hover:bg-neutral-800/50 hover:text-white'
              }`
            }
          >
            <div className="flex items-center">
              <item.icon className="mr-3 h-5 w-5 flex-shrink-0" aria-hidden="true" />
              <span>{item.name}</span>
            </div>
            {item.badge && (
              <span className="badge-info text-[10px] px-2 py-0.5">
                {item.badge}
              </span>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Quick Stats */}
      <div className="px-4 py-4 mx-3 mb-3 bg-gradient-to-br from-primary-900/30 to-transparent border border-primary-700/30 rounded-lg">
        <div className="flex items-center mb-2">
          <SparklesIcon className="w-4 h-4 text-primary-400 mr-2" />
          <p className="text-xs font-semibold text-neutral-200">System Status</p>
        </div>
        <div className="space-y-1 text-xs">
          <div className="flex justify-between text-neutral-400">
            <span>API</span>
            <span className="text-success-400 flex items-center">
              <span className="w-1.5 h-1.5 bg-success-400 rounded-full mr-1 animate-pulse"></span>
              Online
            </span>
          </div>
          <div className="flex justify-between text-neutral-400">
            <span>Models</span>
            <span className="text-primary-400">6 Active</span>
          </div>
          <div className="flex justify-between text-neutral-400">
            <span>Data</span>
            <span className="text-neutral-200">41.2K Records</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-neutral-700/50 bg-neutral-900/50">
        <div className="text-xs text-neutral-500 text-center">
          <p className="font-semibold text-neutral-400">Bank Marketing Analytics</p>
          <p className="mt-1">v1.0.0 | 2025</p>
        </div>
      </div>
    </div>
  );
}

