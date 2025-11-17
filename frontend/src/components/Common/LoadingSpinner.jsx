import React from 'react';

export default function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[500px] animate-fade-in">
      <div className="relative">
        {/* Outer ring */}
        <div className="animate-spin rounded-full h-20 w-20 border-4 border-primary-200"></div>
        {/* Inner spinning ring */}
        <div className="absolute top-0 left-0 animate-spin rounded-full h-20 w-20 border-4 border-transparent border-t-primary-600"></div>
        {/* Center dot */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-primary-600 rounded-full animate-pulse"></div>
      </div>
      <p className="mt-6 text-neutral-600 font-medium text-lg">{message}</p>
      <p className="mt-2 text-neutral-400 text-sm">Please wait while we analyze your data</p>
      {/* Progress dots */}
      <div className="flex gap-2 mt-4">
        <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
    </div>
  );
}

