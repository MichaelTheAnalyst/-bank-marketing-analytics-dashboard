"""
Flask API Backend for Bank Marketing Dashboard
Provides REST endpoints for all analyses
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_and_prepare_data
from feature_importance import run_feature_importance_analysis
from predictive_models import run_predictive_modeling
from customer_segmentation import run_customer_segmentation
from contact_optimization import run_contact_optimization
from economic_impact import run_economic_impact_analysis

import json
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables to cache data
loader = None
df = None
df_encoded = None
X_train = None
X_test = None
y_train = None
y_test = None
feature_names = None

# Data file path
DATA_PATH = r"C:\Users\mn3g24\OneDrive - University of Southampton\Desktop\projects\Bank Maketing 2\bank-additional-full.csv"


def initialize_data():
    """Load and prepare data on startup"""
    global loader, df, df_encoded, X_train, X_test, y_train, y_test, feature_names
    
    print("Loading data...")
    loader = load_and_prepare_data(DATA_PATH)
    df = loader.df
    df_encoded = loader.df_encoded
    X_train, X_test, y_train, y_test, feature_names = loader.get_train_test_split(exclude_duration=True)
    print(f"Data loaded successfully! {len(df)} records")


def convert_to_serializable(obj):
    """Convert numpy/pandas objects to JSON serializable format"""
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, 'tolist'):
        return obj.tolist()
    return obj


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})


@app.route('/api/overview', methods=['GET'])
def get_overview():
    """Get dataset overview statistics"""
    try:
        overview = {
            'total_customers': int(len(df)),
            'conversions': int(df['y_binary'].sum()),
            'conversion_rate': float(df['y_binary'].mean() * 100),
            'avg_contacts': float(df['campaign'].mean()),
            'unique_months': int(df['month'].nunique()),
            'age_stats': {
                'min': int(df['age'].min()),
                'max': int(df['age'].max()),
                'mean': float(df['age'].mean()),
                'median': float(df['age'].median())
            },
            'target_distribution': df['y'].value_counts().to_dict(),
            'job_distribution': df['job'].value_counts().head(10).to_dict(),
            'education_distribution': df['education'].value_counts().to_dict(),
            'marital_distribution': df['marital'].value_counts().to_dict(),
            'contact_distribution': df['contact'].value_counts().to_dict()
        }
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/overview/age-distribution', methods=['GET'])
def get_age_distribution():
    """Get age distribution data"""
    try:
        age_data = df.groupby(['age', 'y']).size().reset_index(name='count')
        return jsonify(age_data.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feature-importance', methods=['GET'])
def get_feature_importance():
    """Get feature importance analysis"""
    try:
        print("Running feature importance analysis...")
        analyzer = run_feature_importance_analysis(X_train, X_test, y_train, y_test, feature_names)
        
        # Get aggregated importance
        aggregated = analyzer.get_aggregated_importance()
        
        # Get individual method results
        rf_importance = analyzer.importance_results.get('random_forest')
        gb_importance = analyzer.importance_results.get('gradient_boosting')
        lr_importance = analyzer.importance_results.get('logistic_regression')
        
        result = {
            'aggregated': aggregated.head(15).to_dict('records'),
            'random_forest': rf_importance.head(15).to_dict('records') if rf_importance is not None else [],
            'gradient_boosting': gb_importance.head(15).to_dict('records') if gb_importance is not None else [],
            'logistic_regression': lr_importance.head(15).to_dict('records') if lr_importance is not None else []
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictive-models', methods=['GET'])
def get_predictive_models():
    """Get predictive model results"""
    try:
        print("Training predictive models...")
        modeler = run_predictive_modeling(X_train, X_test, y_train, y_test, feature_names)
        
        # Get metrics
        metrics_df = modeler.get_metrics_comparison()
        
        # Get confusion matrices for each model
        confusion_matrices = {}
        for model_name in modeler.models.keys():
            from sklearn.metrics import confusion_matrix
            y_pred = modeler.predictions[model_name]['y_pred']
            cm = confusion_matrix(y_test, y_pred)
            confusion_matrices[model_name] = cm.tolist()
        
        # Get ROC curve data
        roc_curves = {}
        for model_name, pred_dict in modeler.predictions.items():
            if pred_dict['y_pred_proba'] is not None:
                from sklearn.metrics import roc_curve, roc_auc_score
                fpr, tpr, _ = roc_curve(y_test, pred_dict['y_pred_proba'])
                auc = roc_auc_score(y_test, pred_dict['y_pred_proba'])
                roc_curves[model_name] = {
                    'fpr': fpr.tolist(),
                    'tpr': tpr.tolist(),
                    'auc': float(auc)
                }
        
        result = {
            'metrics': metrics_df.to_dict('index'),
            'confusion_matrices': confusion_matrices,
            'roc_curves': roc_curves
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/customer-segmentation', methods=['GET'])
def get_customer_segmentation():
    """Get customer segmentation analysis"""
    try:
        n_clusters = int(request.args.get('n_clusters', 4))
        print(f"Running customer segmentation with {n_clusters} clusters...")
        
        segmenter = run_customer_segmentation(df.copy(), n_clusters=n_clusters)
        
        # Get segment analysis
        segment_df = segmenter.analyze_segments()
        
        # Get segment visualization data (PCA)
        from sklearn.decomposition import PCA
        X_scaled, _ = segmenter.prepare_clustering_features()
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        pca_data = {
            'pc1': X_pca[:, 0].tolist(),
            'pc2': X_pca[:, 1].tolist(),
            'segment': segmenter.df['segment'].tolist(),
            'subscribed': segmenter.df['y'].tolist(),
            'explained_variance': pca.explained_variance_ratio_.tolist()
        }
        
        result = {
            'segments': segment_df.to_dict('records'),
            'pca_data': pca_data
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contact-optimization', methods=['GET'])
def get_contact_optimization():
    """Get contact optimization analysis"""
    try:
        print("Running contact optimization analysis...")
        optimizer = run_contact_optimization(df.copy())
        
        # Frequency analysis
        freq_analysis = optimizer.analyze_contact_frequency()
        
        # Timing analysis
        month_analysis, day_analysis = optimizer.analyze_contact_timing()
        
        # Channel analysis
        channel_analysis = optimizer.analyze_contact_channel()
        
        # Previous outcome analysis
        outcome_analysis = optimizer.analyze_previous_outcome_impact()
        
        result = {
            'frequency': freq_analysis.to_dict('records'),
            'timing': {
                'by_month': month_analysis.to_dict('records'),
                'by_day': day_analysis.to_dict('records')
            },
            'channel': channel_analysis.to_dict('records'),
            'previous_outcome': outcome_analysis.to_dict('records')
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/economic-impact', methods=['GET'])
def get_economic_impact():
    """Get economic impact analysis"""
    try:
        print("Running economic impact analysis...")
        econ_analyzer = run_economic_impact_analysis(df.copy())
        
        # Correlation analysis
        corr_df = econ_analyzer.analyze_economic_correlations()
        
        # Economic conditions analysis
        econ_conditions = econ_analyzer.analyze_economic_conditions_segments()
        
        # Monthly trends
        month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        economic_indicators = ['emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 
                             'euribor3m', 'nr.employed']
        monthly_data = df.groupby('month')[economic_indicators + ['y_binary']].mean().reset_index()
        
        result = {
            'correlations': corr_df.to_dict('records'),
            'conditions': econ_conditions.to_dict('records'),
            'monthly_trends': monthly_data.to_dict('records')
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    initialize_data()
    print("\n" + "="*50)
    print("🚀 Bank Marketing API Server")
    print("="*50)
    print("API running on http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')

