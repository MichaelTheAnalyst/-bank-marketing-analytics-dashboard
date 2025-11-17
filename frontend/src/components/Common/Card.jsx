import React from 'react';

export default function Card({ children, className = '', hover = false }) {
  return (
    <div
      className={`${hover ? 'premium-card-hover' : 'premium-card'} p-6 animate-fade-in ${className}`}
    >
      {children}
    </div>
  );
}

export function MetricCard({ title, value, icon: Icon, color = 'primary', trend }) {
  const colorClasses = {
    primary: 'from-primary-500 to-primary-700',
    success: 'from-success-500 to-success-700',
    warning: 'from-warning-500 to-warning-700',
    danger: 'from-secondary-500 to-secondary-700',
    info: 'from-primary-400 to-primary-600',
  };

  const bgClasses = {
    primary: 'bg-primary-50',
    success: 'bg-success-50',
    warning: 'bg-warning-50',
    danger: 'bg-secondary-50',
    info: 'bg-primary-50',
  };

  return (
    <div className="metric-card group animate-slide-up">
      <div className="flex items-center justify-between relative z-10">
        <div className="flex-1">
          <p className="text-xs font-semibold text-neutral-500 uppercase tracking-wide mb-2">{title}</p>
          <p className="text-4xl font-bold text-neutral-900 font-display">{value}</p>
          {trend && (
            <div className="flex items-center mt-3">
              <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-semibold ${
                trend.positive ? 'bg-success-100 text-success-700' : 'bg-secondary-100 text-secondary-700'
              }`}>
                {trend.positive ? '↑' : '↓'} {trend.value}
              </span>
            </div>
          )}
        </div>
        {Icon && (
          <div className={`relative p-4 rounded-2xl bg-gradient-to-br ${colorClasses[color]} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
            <Icon className="h-8 w-8 text-white" />
            <div className={`absolute inset-0 ${bgClasses[color]} opacity-20 rounded-2xl blur-xl group-hover:opacity-30 transition-opacity`}></div>
          </div>
        )}
      </div>
      {/* Decorative gradient */}
      <div className={`absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-br ${colorClasses[color]} opacity-5 rounded-full blur-3xl -z-0`}></div>
    </div>
  );
}

