"""
Predictive Modeling Module
Build and evaluate realistic predictive models (excluding duration)
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (classification_report, confusion_matrix, roc_auc_score, 
                            roc_curve, precision_recall_curve, average_precision_score,
                            accuracy_score, precision_score, recall_score, f1_score)
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')


class PredictiveModeler:
    """Build and evaluate multiple predictive models"""
    
    def __init__(self, X_train, X_test, y_train, y_test, feature_names):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = feature_names
        self.models = {}
        self.predictions = {}
        self.metrics = {}
        
    def handle_imbalance(self, method='smote'):
        """Handle class imbalance"""
        if method == 'smote':
            print("Applying SMOTE to handle class imbalance...")
            smote = SMOTE(random_state=42)
            X_train_balanced, y_train_balanced = smote.fit_resample(self.X_train, self.y_train)
            return X_train_balanced, y_train_balanced
        return self.X_train, self.y_train
    
    def train_all_models(self, use_smote=True):
        """Train all classification models"""
        print("Training models...")
        
        # Handle imbalance if requested
        if use_smote:
            X_train, y_train = self.handle_imbalance('smote')
        else:
            X_train, y_train = self.X_train, self.y_train
        
        # Define models
        models_to_train = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42, class_weight='balanced', max_depth=10),
            'KNN': KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            'Naive Bayes': GaussianNB()
        }
        
        # Train each model
        for name, model in models_to_train.items():
            print(f"  Training {name}...")
            model.fit(X_train, y_train)
            self.models[name] = model
            
            # Get predictions
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            self.predictions[name] = {
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            # Calculate metrics
            self.metrics[name] = self._calculate_metrics(y_pred, y_pred_proba)
        
        print("All models trained successfully!")
        return self.metrics
    
    def _calculate_metrics(self, y_pred, y_pred_proba):
        """Calculate comprehensive metrics"""
        metrics = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, zero_division=0),
            'recall': recall_score(self.y_test, y_pred, zero_division=0),
            'f1': f1_score(self.y_test, y_pred, zero_division=0)
        }
        
        if y_pred_proba is not None:
            metrics['roc_auc'] = roc_auc_score(self.y_test, y_pred_proba)
            metrics['avg_precision'] = average_precision_score(self.y_test, y_pred_proba)
        
        return metrics
    
    def get_metrics_comparison(self):
        """Get comparison table of all model metrics"""
        if not self.metrics:
            raise ValueError("No models trained yet. Call train_all_models() first.")
        
        metrics_df = pd.DataFrame(self.metrics).T
        metrics_df = metrics_df.round(4)
        metrics_df = metrics_df.sort_values('f1', ascending=False)
        
        return metrics_df
    
    def plot_metrics_comparison(self):
        """Plot comparison of model metrics"""
        metrics_df = self.get_metrics_comparison()
        
        # Prepare data for plotting
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1']
        if 'roc_auc' in metrics_df.columns:
            metrics_to_plot.append('roc_auc')
        
        fig = go.Figure()
        
        for metric in metrics_to_plot:
            fig.add_trace(go.Bar(
                name=metric.upper().replace('_', ' '),
                x=metrics_df.index,
                y=metrics_df[metric],
                text=metrics_df[metric].round(3),
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Model Performance Comparison',
            xaxis_title='Model',
            yaxis_title='Score',
            barmode='group',
            height=500,
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def plot_roc_curves(self):
        """Plot ROC curves for all models"""
        fig = go.Figure()
        
        for name, pred_dict in self.predictions.items():
            if pred_dict['y_pred_proba'] is not None:
                fpr, tpr, _ = roc_curve(self.y_test, pred_dict['y_pred_proba'])
                auc = roc_auc_score(self.y_test, pred_dict['y_pred_proba'])
                
                fig.add_trace(go.Scatter(
                    x=fpr, y=tpr,
                    name=f'{name} (AUC={auc:.3f})',
                    mode='lines'
                ))
        
        # Add diagonal line
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            name='Random Classifier',
            mode='lines',
            line=dict(dash='dash', color='gray')
        ))
        
        fig.update_layout(
            title='ROC Curves - Model Comparison',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            height=500,
            template='plotly_white',
            legend=dict(orientation="v", yanchor="bottom", y=0.02, xanchor="right", x=0.98)
        )
        
        return fig
    
    def plot_precision_recall_curves(self):
        """Plot Precision-Recall curves"""
        fig = go.Figure()
        
        for name, pred_dict in self.predictions.items():
            if pred_dict['y_pred_proba'] is not None:
                precision, recall, _ = precision_recall_curve(self.y_test, pred_dict['y_pred_proba'])
                avg_precision = average_precision_score(self.y_test, pred_dict['y_pred_proba'])
                
                fig.add_trace(go.Scatter(
                    x=recall, y=precision,
                    name=f'{name} (AP={avg_precision:.3f})',
                    mode='lines'
                ))
        
        fig.update_layout(
            title='Precision-Recall Curves',
            xaxis_title='Recall',
            yaxis_title='Precision',
            height=500,
            template='plotly_white',
            legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="right", x=0.98)
        )
        
        return fig
    
    def plot_confusion_matrix(self, model_name='Random Forest'):
        """Plot confusion matrix for a specific model"""
        if model_name not in self.predictions:
            raise ValueError(f"Model {model_name} not found")
        
        y_pred = self.predictions[model_name]['y_pred']
        cm = confusion_matrix(self.y_test, y_pred)
        
        # Calculate percentages
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Create annotations
        annotations = []
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                annotations.append(
                    f"{cm[i, j]}<br>({cm_percent[i, j]:.1f}%)"
                )
        
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted No', 'Predicted Yes'],
            y=['Actual No', 'Actual Yes'],
            colorscale='Blues',
            text=np.array(annotations).reshape(cm.shape),
            texttemplate='%{text}',
            textfont={"size": 14},
            showscale=True
        ))
        
        fig.update_layout(
            title=f'Confusion Matrix - {model_name}',
            xaxis_title='Predicted Label',
            yaxis_title='True Label',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def get_model_insights(self):
        """Generate insights about model performance"""
        metrics_df = self.get_metrics_comparison()
        best_model = metrics_df.index[0]
        best_f1 = metrics_df.loc[best_model, 'f1']
        
        insights = []
        insights.append("### 🎯 Model Performance Insights\n")
        insights.append(f"**Best Performing Model:** {best_model} (F1-Score: {best_f1:.3f})")
        insights.append("")
        
        # Get best model's detailed metrics
        best_metrics = metrics_df.loc[best_model]
        insights.append(f"- **Accuracy:** {best_metrics['accuracy']:.1%} - Overall correctness")
        insights.append(f"- **Precision:** {best_metrics['precision']:.1%} - When we predict 'Yes', we're right {best_metrics['precision']:.1%} of the time")
        insights.append(f"- **Recall:** {best_metrics['recall']:.1%} - We capture {best_metrics['recall']:.1%} of actual subscribers")
        insights.append(f"- **F1-Score:** {best_metrics['f1']:.3f} - Balanced performance metric")
        
        if 'roc_auc' in best_metrics:
            insights.append(f"- **ROC-AUC:** {best_metrics['roc_auc']:.3f} - Discrimination ability")
        
        insights.append("\n**💡 Business Implications:**")
        
        # Calculate expected performance on new data
        total_customers = len(self.y_test)
        actual_positives = self.y_test.sum()
        
        insights.append(f"- Out of 1,000 customers contacted, expect to identify ~{int(best_metrics['recall'] * (actual_positives/total_customers) * 1000)} potential subscribers")
        insights.append(f"- Campaign efficiency: {best_metrics['precision']:.1%} of targeted customers likely to subscribe")
        insights.append(f"- **This model excludes call duration**, making it useful for pre-call prioritization")
        
        return "\n".join(insights)


def run_predictive_modeling(X_train, X_test, y_train, y_test, feature_names):
    """Run complete predictive modeling pipeline"""
    modeler = PredictiveModeler(X_train, X_test, y_train, y_test, feature_names)
    modeler.train_all_models(use_smote=True)
    return modeler


if __name__ == "__main__":
    print("Predictive Modeling Module - Run via dashboard")


