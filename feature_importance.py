"""
Feature Importance Analysis Module
Identifies key drivers of term deposit subscription
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
import warnings
warnings.filterwarnings('ignore')


class FeatureImportanceAnalyzer:
    """Analyze feature importance using multiple methods"""
    
    def __init__(self, X_train, X_test, y_train, y_test, feature_names):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = feature_names
        self.importance_results = {}
        
    def random_forest_importance(self):
        """Get feature importance from Random Forest"""
        print("Calculating Random Forest feature importance...")
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(self.X_train, self.y_train)
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.importance_results['random_forest'] = importance_df
        return importance_df
    
    def gradient_boosting_importance(self):
        """Get feature importance from Gradient Boosting"""
        print("Calculating Gradient Boosting feature importance...")
        gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
        gb.fit(self.X_train, self.y_train)
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': gb.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.importance_results['gradient_boosting'] = importance_df
        return importance_df
    
    def logistic_regression_importance(self):
        """Get feature importance from Logistic Regression (coefficients)"""
        print("Calculating Logistic Regression feature importance...")
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(self.X_train, self.y_train)
        
        # Use absolute coefficients as importance
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': np.abs(lr.coef_[0])
        }).sort_values('importance', ascending=False)
        
        self.importance_results['logistic_regression'] = importance_df
        return importance_df
    
    def permutation_importance_analysis(self):
        """Calculate permutation importance"""
        print("Calculating Permutation importance...")
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(self.X_train, self.y_train)
        
        perm_importance = permutation_importance(
            rf, self.X_test, self.y_test, n_repeats=10, random_state=42, n_jobs=-1
        )
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': perm_importance.importances_mean,
            'std': perm_importance.importances_std
        }).sort_values('importance', ascending=False)
        
        self.importance_results['permutation'] = importance_df
        return importance_df
    
    def get_aggregated_importance(self):
        """Aggregate importance across all methods"""
        if not self.importance_results:
            self.random_forest_importance()
            self.gradient_boosting_importance()
            self.logistic_regression_importance()
        
        # Normalize each importance to 0-1 scale
        normalized_results = []
        for method, df in self.importance_results.items():
            df_norm = df.copy()
            df_norm['importance'] = df_norm['importance'] / df_norm['importance'].sum()
            df_norm['method'] = method
            normalized_results.append(df_norm)
        
        # Combine and average
        combined_df = pd.concat(normalized_results)
        aggregated = combined_df.groupby('feature')['importance'].mean().reset_index()
        aggregated = aggregated.sort_values('importance', ascending=False)
        
        return aggregated
    
    def plot_feature_importance(self, method='aggregated', top_n=15):
        """Create interactive bar plot of feature importance"""
        if method == 'aggregated':
            df = self.get_aggregated_importance()
            title = f"Top {top_n} Features - Aggregated Importance"
        else:
            if method not in self.importance_results:
                raise ValueError(f"Method {method} not calculated yet")
            df = self.importance_results[method]
            title = f"Top {top_n} Features - {method.replace('_', ' ').title()} Importance"
        
        df_top = df.head(top_n)
        
        # Clean feature names for display
        df_top['feature_display'] = df_top['feature'].str.replace('_encoded', '').str.replace('_', ' ').str.title()
        
        fig = go.Figure(go.Bar(
            x=df_top['importance'],
            y=df_top['feature_display'],
            orientation='h',
            marker=dict(
                color=df_top['importance'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Importance")
            ),
            text=df_top['importance'].round(4),
            textposition='auto'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Importance Score",
            yaxis_title="Feature",
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white'
        )
        
        return fig
    
    def plot_importance_comparison(self, top_n=10):
        """Compare feature importance across different methods"""
        # Ensure all methods are calculated
        if len(self.importance_results) < 3:
            self.random_forest_importance()
            self.gradient_boosting_importance()
            self.logistic_regression_importance()
        
        # Get top features from aggregated importance
        aggregated = self.get_aggregated_importance()
        top_features = aggregated.head(top_n)['feature'].tolist()
        
        # Prepare data for comparison
        comparison_data = []
        for method, df in self.importance_results.items():
            df_filtered = df[df['feature'].isin(top_features)].copy()
            # Normalize
            df_filtered['importance_norm'] = df_filtered['importance'] / df_filtered['importance'].sum()
            df_filtered['method'] = method.replace('_', ' ').title()
            comparison_data.append(df_filtered)
        
        comparison_df = pd.concat(comparison_data)
        comparison_df['feature_display'] = comparison_df['feature'].str.replace('_encoded', '').str.replace('_', ' ').str.title()
        
        fig = px.bar(
            comparison_df,
            x='feature_display',
            y='importance_norm',
            color='method',
            barmode='group',
            title=f'Feature Importance Comparison Across Methods (Top {top_n})',
            labels={'feature_display': 'Feature', 'importance_norm': 'Normalized Importance', 'method': 'Method'},
            template='plotly_white'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def get_feature_insights(self, df_original):
        """Generate insights about top features"""
        aggregated = self.get_aggregated_importance()
        top_5_features = aggregated.head(5)['feature'].tolist()
        
        insights = []
        insights.append("### 🔍 Key Feature Insights\n")
        
        for i, feature in enumerate(top_5_features, 1):
            # Clean feature name
            feature_clean = feature.replace('_encoded', '')
            
            insight = f"**{i}. {feature_clean.replace('_', ' ').title()}** - "
            
            # Add context-specific insights
            if 'euribor' in feature.lower():
                insight += "Economic indicator (interest rate) - strongly influences customer financial decisions"
            elif 'nr.employed' in feature.lower():
                insight += "Employment levels - reflects overall economic health and consumer confidence"
            elif 'emp.var.rate' in feature.lower():
                insight += "Employment variation rate - indicates economic stability/volatility"
            elif 'cons' in feature.lower() and 'idx' in feature.lower():
                insight += "Consumer sentiment indicator - affects willingness to save/invest"
            elif 'poutcome' in feature.lower():
                insight += "Previous campaign outcome - strong predictor of current response"
            elif 'month' in feature.lower():
                insight += "Timing of contact - seasonal patterns in subscription behavior"
            elif 'contact' in feature.lower():
                insight += "Communication channel - cellular vs telephone effectiveness"
            elif 'age' in feature.lower():
                insight += "Customer age - different life stages have different financial priorities"
            elif 'job' in feature.lower():
                insight += "Occupation type - indicates income level and financial stability"
            elif 'education' in feature.lower():
                insight += "Education level - correlates with financial literacy and investment behavior"
            elif 'pdays' in feature.lower():
                insight += "Days since last contact - recency effect on conversion"
            elif 'previous' in feature.lower():
                insight += "Number of previous contacts - engagement history matters"
            elif 'campaign' in feature.lower():
                insight += "Current campaign contacts - balance between persistence and annoyance"
            else:
                insight += "Important predictor of subscription behavior"
            
            insights.append(insight)
        
        return "\n\n".join(insights)


def run_feature_importance_analysis(X_train, X_test, y_train, y_test, feature_names):
    """Run complete feature importance analysis"""
    analyzer = FeatureImportanceAnalyzer(X_train, X_test, y_train, y_test, feature_names)
    
    # Calculate all importance metrics
    analyzer.random_forest_importance()
    analyzer.gradient_boosting_importance()
    analyzer.logistic_regression_importance()
    
    return analyzer


if __name__ == "__main__":
    print("Feature Importance Analysis Module - Run via dashboard")


