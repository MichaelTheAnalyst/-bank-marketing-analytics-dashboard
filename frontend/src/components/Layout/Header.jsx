import React from 'react';
import { BellIcon, Cog6ToothIcon, ChartBarSquareIcon } from '@heroicons/react/24/outline';

export default function Header() {
  return (
    <div className="bg-white/80 backdrop-blur-md shadow-soft border-b border-neutral-200/50">
      <div className="flex items-center justify-between h-20 px-8">
        {/* Page Title */}
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center shadow-lg">
            <ChartBarSquareIcon className="w-7 h-7 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gradient font-display">
              Campaign Analytics Dashboard
            </h2>
            <p className="text-sm text-neutral-600 mt-0.5">
              Direct marketing campaigns analysis for term deposit subscriptions
            </p>
            <p className="text-xs text-neutral-400 mt-0.5 flex items-center">
              <span className="inline-block w-1.5 h-1.5 bg-primary-500 rounded-full mr-1.5"></span>
              Created by <span className="font-semibold text-neutral-600 ml-1">Masood Nazari</span>
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-3">
          {/* Notifications */}
          <button className="relative p-2.5 text-neutral-600 hover:text-primary-600 rounded-xl hover:bg-primary-50 transition-all duration-200 group">
            <BellIcon className="h-5 w-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-secondary-500 rounded-full animate-pulse"></span>
            <span className="absolute inset-0 rounded-xl bg-primary-100 opacity-0 group-hover:opacity-100 transition-opacity duration-200 -z-10"></span>
          </button>

          {/* Settings */}
          <button className="relative p-2.5 text-neutral-600 hover:text-primary-600 rounded-xl hover:bg-primary-50 transition-all duration-200 group">
            <Cog6ToothIcon className="h-5 w-5" />
            <span className="absolute inset-0 rounded-xl bg-primary-100 opacity-0 group-hover:opacity-100 transition-opacity duration-200 -z-10"></span>
          </button>

          {/* User Profile */}
          <div className="flex items-center space-x-3 ml-3 pl-3 border-l border-neutral-200">
            <div className="text-right">
              <p className="text-sm font-semibold text-neutral-800">Masood Nazari</p>
              <p className="text-xs text-neutral-500">Data Scientist</p>
            </div>
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-md">
                MN
              </div>
              <span className="absolute bottom-0 right-0 w-3 h-3 bg-success-500 border-2 border-white rounded-full"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

