"""
Customer Segmentation Analysis Module
Identify distinct customer segments and their characteristics
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')


class CustomerSegmentation:
    """Perform customer segmentation analysis"""
    
    def __init__(self, df):
        self.df = df
        self.segments = None
        self.cluster_model = None
        
    def prepare_clustering_features(self):
        """Prepare features for clustering"""
        # Select relevant numeric and encoded features
        clustering_features = [
            'age', 'campaign', 'previous',
            'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
            'euribor3m', 'nr.employed'
        ]
        
        # Add encoded categorical features
        encoded_cats = [col for col in self.df.columns if col.endswith('_encoded')]
        clustering_features.extend(encoded_cats)
        
        # Create feature matrix
        X = self.df[clustering_features].copy()
        
        # Handle any missing values
        X = X.fillna(X.median())
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        return X_scaled, clustering_features
    
    def find_optimal_clusters(self, max_clusters=10):
        """Use elbow method to find optimal number of clusters"""
        X_scaled, _ = self.prepare_clustering_features()
        
        inertias = []
        silhouette_scores = []
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
        
        # Plot elbow curve
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(K_range), y=inertias,
            mode='lines+markers',
            name='Inertia',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Elbow Method for Optimal K',
            xaxis_title='Number of Clusters (K)',
            yaxis_title='Inertia',
            template='plotly_white',
            height=400
        )
        
        return fig, inertias
    
    def perform_clustering(self, n_clusters=4):
        """Perform K-Means clustering"""
        print(f"Performing clustering with {n_clusters} clusters...")
        
        X_scaled, feature_names = self.prepare_clustering_features()
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.df['segment'] = kmeans.fit_predict(X_scaled)
        self.cluster_model = kmeans
        
        print("Clustering complete!")
        return self.df['segment']
    
    def analyze_segments(self):
        """Analyze characteristics of each segment"""
        if 'segment' not in self.df.columns:
            self.perform_clustering()
        
        segment_analysis = []
        
        for segment in sorted(self.df['segment'].unique()):
            segment_data = self.df[self.df['segment'] == segment]
            
            analysis = {
                'Segment': f"Segment {segment}",
                'Size': len(segment_data),
                'Size %': f"{len(segment_data) / len(self.df) * 100:.1f}%",
                'Conversion Rate': f"{segment_data['y_binary'].mean() * 100:.1f}%",
                'Avg Age': f"{segment_data['age'].mean():.1f}",
                'Avg Campaign Contacts': f"{segment_data['campaign'].mean():.1f}",
                'Previously Contacted %': f"{segment_data['previously_contacted'].mean() * 100:.1f}%",
                'Has Housing Loan %': f"{(segment_data['housing'] == 'yes').mean() * 100:.1f}%",
                'Has Personal Loan %': f"{(segment_data['loan'] == 'yes').mean() * 100:.1f}%",
                'Top Job': segment_data['job'].mode()[0] if len(segment_data['job'].mode()) > 0 else 'N/A',
                'Top Education': segment_data['education'].mode()[0] if len(segment_data['education'].mode()) > 0 else 'N/A',
                'Top Marital': segment_data['marital'].mode()[0] if len(segment_data['marital'].mode()) > 0 else 'N/A'
            }
            
            segment_analysis.append(analysis)
        
        return pd.DataFrame(segment_analysis)
    
    def plot_segment_characteristics(self):
        """Plot key characteristics of each segment"""
        if 'segment' not in self.df.columns:
            self.perform_clustering()
        
        segment_stats = self.df.groupby('segment').agg({
            'age': 'mean',
            'campaign': 'mean',
            'previous': 'mean',
            'y_binary': 'mean',
            'segment': 'count'
        }).rename(columns={'segment': 'count'})
        
        segment_stats['conversion_rate'] = segment_stats['y_binary'] * 100
        segment_stats = segment_stats.round(2)
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Segment Size', 'Conversion Rate %', 'Average Age', 'Avg Campaign Contacts'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        segments = segment_stats.index.astype(str)
        
        # Segment size
        fig.add_trace(
            go.Bar(x=segments, y=segment_stats['count'], name='Size', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Conversion rate
        fig.add_trace(
            go.Bar(x=segments, y=segment_stats['conversion_rate'], name='Conv. Rate', marker_color='lightgreen'),
            row=1, col=2
        )
        
        # Average age
        fig.add_trace(
            go.Bar(x=segments, y=segment_stats['age'], name='Age', marker_color='lightsalmon'),
            row=2, col=1
        )
        
        # Campaign contacts
        fig.add_trace(
            go.Bar(x=segments, y=segment_stats['campaign'], name='Contacts', marker_color='lightpink'),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="Segment", row=1, col=1)
        fig.update_xaxes(title_text="Segment", row=1, col=2)
        fig.update_xaxes(title_text="Segment", row=2, col=1)
        fig.update_xaxes(title_text="Segment", row=2, col=2)
        
        fig.update_layout(
            title_text="Customer Segment Characteristics",
            showlegend=False,
            height=600,
            template='plotly_white'
        )
        
        return fig
    
    def plot_segments_2d(self):
        """Plot segments in 2D using PCA"""
        if 'segment' not in self.df.columns:
            self.perform_clustering()
        
        X_scaled, _ = self.prepare_clustering_features()
        
        # Apply PCA for visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        # Create scatter plot
        plot_df = pd.DataFrame({
            'PC1': X_pca[:, 0],
            'PC2': X_pca[:, 1],
            'Segment': self.df['segment'].astype(str),
            'Subscribed': self.df['y']
        })
        
        fig = px.scatter(
            plot_df,
            x='PC1', y='PC2',
            color='Segment',
            symbol='Subscribed',
            title=f'Customer Segments Visualization (PCA)<br><sub>Explained Variance: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}</sub>',
            labels={'PC1': f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%})',
                   'PC2': f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%})'},
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def get_segment_profiles(self):
        """Generate detailed segment profiles"""
        if 'segment' not in self.df.columns:
            self.perform_clustering()
        
        profiles = []
        
        for segment in sorted(self.df['segment'].unique()):
            segment_data = self.df[self.df['segment'] == segment]
            conv_rate = segment_data['y_binary'].mean()
            
            profile = f"### 📊 Segment {segment}\n"
            profile += f"**Size:** {len(segment_data):,} customers ({len(segment_data)/len(self.df)*100:.1f}%)\n"
            profile += f"**Conversion Rate:** {conv_rate*100:.1f}%\n\n"
            
            # Determine segment persona
            avg_age = segment_data['age'].mean()
            top_job = segment_data['job'].mode()[0]
            top_education = segment_data['education'].mode()[0]
            has_loans = (segment_data['housing'] == 'yes').mean()
            prev_contacted = segment_data['previously_contacted'].mean()
            
            profile += "**Persona:** "
            if conv_rate > 0.15:
                profile += "🌟 **High-Value Targets** - "
            elif conv_rate > 0.08:
                profile += "💼 **Moderate Potential** - "
            else:
                profile += "📉 **Low Converters** - "
            
            profile += f"Typically {int(avg_age)} years old, working in {top_job}, "
            profile += f"with {top_education} education. "
            
            if has_loans > 0.5:
                profile += "Most have existing loans. "
            
            if prev_contacted > 0.5:
                profile += "Frequently contacted in previous campaigns."
            else:
                profile += "Mostly new contacts."
            
            profile += "\n\n**Recommendation:** "
            if conv_rate > 0.15:
                profile += "Prioritize this segment - high ROI potential. Allocate more resources."
            elif conv_rate > 0.08:
                profile += "Moderate priority - selective targeting with personalized approach."
            else:
                profile += "Low priority - consider alternative channels or skip unless capacity allows."
            
            profiles.append(profile)
        
        return "\n\n---\n\n".join(profiles)


def run_customer_segmentation(df, n_clusters=4):
    """Run complete customer segmentation analysis"""
    segmenter = CustomerSegmentation(df)
    segmenter.perform_clustering(n_clusters=n_clusters)
    return segmenter


if __name__ == "__main__":
    print("Customer Segmentation Module - Run via dashboard")


