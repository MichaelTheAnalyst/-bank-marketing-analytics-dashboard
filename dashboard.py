"""
Bank Marketing Campaign Analysis Dashboard
Comprehensive dashboard for analyzing bank marketing campaign data
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Import custom modules
from data_loader import load_and_prepare_data
from feature_importance import run_feature_importance_analysis
from predictive_models import run_predictive_modeling
from customer_segmentation import run_customer_segmentation
from contact_optimization import run_contact_optimization
from economic_impact import run_economic_impact_analysis

# Page configuration
st.set_page_config(
    page_title="Bank Marketing Analytics Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ecc71;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(filepath):
    """Load and cache the data"""
    loader = load_and_prepare_data(filepath)
    return loader


@st.cache_data
def get_train_test_data(_loader):
    """Get and cache train/test split"""
    return _loader.get_train_test_split(exclude_duration=True)


def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 Bank Marketing Campaign Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; color: #7f8c8d;'>
            Comprehensive analysis of direct marketing campaigns for term deposit subscriptions
        </p>
        <p style='font-size: 0.9rem; color: #95a5a6; margin-top: 0.5rem;'>
            Created by Masood Nazari
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
        st.title("📊 Navigation")
        
        # File uploader
        st.subheader("Data Source")
        
        # Default file path
        default_path = r"C:\Users\mn3g24\OneDrive - University of Southampton\Desktop\projects\Bank Maketing 2\bank-additional-full.csv"
        
        use_default = st.checkbox("Use default file path", value=True)
        
        if use_default:
            filepath = default_path
            st.info(f"Using: {Path(filepath).name}")
        else:
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file:
                filepath = uploaded_file
            else:
                st.warning("Please upload a file or use default path")
                return
        
        # Analysis sections
        st.subheader("Analysis Sections")
        sections = {
            "📈 Overview": "overview",
            "⭐ Feature Importance": "feature_importance",
            "🤖 Predictive Models": "predictive_models",
            "👥 Customer Segmentation": "segmentation",
            "📞 Contact Optimization": "contact_optimization",
            "💰 Economic Impact": "economic_impact"
        }
        
        selected_section = st.radio(
            "Select Analysis",
            list(sections.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📝 About
        This dashboard provides comprehensive analysis of bank marketing campaigns including:
        - Feature importance analysis
        - Predictive modeling (realistic, pre-call)
        - Customer segmentation
        - Contact strategy optimization
        - Economic impact assessment
        """)
    
    # Load data
    try:
        with st.spinner("Loading data..."):
            loader = load_data(filepath)
            df = loader.df
            df_encoded = loader.df_encoded
            
        st.success(f"✅ Data loaded successfully! {len(df):,} records")
        
        # Get section to display
        section = sections[selected_section]
        
        # =====================
        # OVERVIEW SECTION
        # =====================
        if section == "overview":
            st.markdown('<h2 class="section-header">📈 Dataset Overview</h2>', unsafe_allow_html=True)
            
            # Key metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            total_customers = len(df)
            conversions = df['y_binary'].sum()
            conversion_rate = df['y_binary'].mean() * 100
            avg_contacts = df['campaign'].mean()
            unique_months = df['month'].nunique()
            
            with col1:
                st.metric("Total Customers", f"{total_customers:,}")
            with col2:
                st.metric("Conversions", f"{conversions:,}")
            with col3:
                st.metric("Conversion Rate", f"{conversion_rate:.2f}%")
            with col4:
                st.metric("Avg Contacts", f"{avg_contacts:.1f}")
            with col5:
                st.metric("Campaign Months", unique_months)
            
            st.markdown("---")
            
            # Two columns for charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Target Variable Distribution")
                target_counts = df['y'].value_counts()
                import plotly.graph_objects as go
                fig = go.Figure(data=[
                    go.Pie(labels=target_counts.index, values=target_counts.values,
                          hole=0.4, marker=dict(colors=['#FF6B6B', '#4ECDC4']))
                ])
                fig.update_layout(height=350, template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Age Distribution")
                import plotly.express as px
                fig = px.histogram(df, x='age', color='y', 
                                  title='Age Distribution by Outcome',
                                  marginal='box',
                                  color_discrete_map={'yes': '#4ECDC4', 'no': '#FF6B6B'},
                                  template='plotly_white')
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional stats
            st.subheader("Dataset Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Demographic Overview**")
                st.write(f"- Age range: {df['age'].min()} - {df['age'].max()} years")
                st.write(f"- Most common job: {df['job'].mode()[0]}")
                st.write(f"- Most common education: {df['education'].mode()[0]}")
                st.write(f"- Marital status: {df['marital'].value_counts().to_dict()}")
            
            with col2:
                st.write("**Campaign Statistics**")
                st.write(f"- Contact methods: {df['contact'].value_counts().to_dict()}")
                st.write(f"- Average call duration: {df['duration'].mean():.0f} seconds")
                st.write(f"- Customers with housing loan: {(df['housing']=='yes').sum():,}")
                st.write(f"- Customers with personal loan: {(df['loan']=='yes').sum():,}")
        
        # =====================
        # FEATURE IMPORTANCE
        # =====================
        elif section == "feature_importance":
            st.markdown('<h2 class="section-header">⭐ Feature Importance Analysis</h2>', 
                       unsafe_allow_html=True)
            
            st.markdown("""
            Understanding which features drive term deposit subscriptions is crucial for:
            - **Targeting**: Focus on customers with favorable characteristics
            - **Campaign Design**: Emphasize the right message at the right time
            - **Resource Allocation**: Invest where it matters most
            """)
            
            with st.spinner("Calculating feature importance..."):
                X_train, X_test, y_train, y_test, feature_names = get_train_test_data(loader)
                analyzer = run_feature_importance_analysis(X_train, X_test, y_train, y_test, feature_names)
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Aggregated Importance", "🔍 Method Comparison", "💡 Insights"])
            
            with tab1:
                st.subheader("Top Features - Aggregated Across Methods")
                fig = analyzer.plot_feature_importance(method='aggregated', top_n=15)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("🔍 This chart shows the most important features averaged across multiple ML algorithms (Random Forest, Gradient Boosting, Logistic Regression)")
            
            with tab2:
                st.subheader("Feature Importance by Method")
                fig = analyzer.plot_importance_comparison(top_n=10)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show individual methods
                col1, col2 = st.columns(2)
                with col1:
                    fig_rf = analyzer.plot_feature_importance(method='random_forest', top_n=10)
                    st.plotly_chart(fig_rf, use_container_width=True)
                
                with col2:
                    fig_gb = analyzer.plot_feature_importance(method='gradient_boosting', top_n=10)
                    st.plotly_chart(fig_gb, use_container_width=True)
            
            with tab3:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                insights = analyzer.get_feature_insights(df)
                st.markdown(insights)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # =====================
        # PREDICTIVE MODELS
        # =====================
        elif section == "predictive_models":
            st.markdown('<h2 class="section-header">🤖 Predictive Models</h2>', 
                       unsafe_allow_html=True)
            
            st.markdown("""
            Build realistic predictive models **without call duration** to enable pre-call customer prioritization.
            These models can be deployed to predict subscription likelihood before any contact is made.
            """)
            
            with st.spinner("Training models... This may take a minute..."):
                X_train, X_test, y_train, y_test, feature_names = get_train_test_data(loader)
                modeler = run_predictive_modeling(X_train, X_test, y_train, y_test, feature_names)
            
            st.success("✅ All models trained successfully!")
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Comparison", "📈 ROC Curves", 
                                              "🎯 Confusion Matrix", "💡 Insights"])
            
            with tab1:
                st.subheader("Model Performance Metrics")
                
                # Metrics table
                metrics_df = modeler.get_metrics_comparison()
                st.dataframe(metrics_df.style.highlight_max(axis=0, color='lightgreen'), 
                           use_container_width=True)
                
                # Chart
                fig = modeler.plot_metrics_comparison()
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("ROC Curves")
                    fig = modeler.plot_roc_curves()
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Precision-Recall Curves")
                    fig = modeler.plot_precision_recall_curves()
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Confusion Matrix")
                
                model_choice = st.selectbox(
                    "Select Model",
                    list(modeler.models.keys())
                )
                
                fig = modeler.plot_confusion_matrix(model_choice)
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed metrics for selected model
                st.write(f"**Detailed Metrics for {model_choice}:**")
                selected_metrics = modeler.metrics[model_choice]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Accuracy", f"{selected_metrics['accuracy']:.3f}")
                with col2:
                    st.metric("Precision", f"{selected_metrics['precision']:.3f}")
                with col3:
                    st.metric("Recall", f"{selected_metrics['recall']:.3f}")
                with col4:
                    st.metric("F1-Score", f"{selected_metrics['f1']:.3f}")
            
            with tab4:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                insights = modeler.get_model_insights()
                st.markdown(insights)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # =====================
        # CUSTOMER SEGMENTATION
        # =====================
        elif section == "segmentation":
            st.markdown('<h2 class="section-header">👥 Customer Segmentation</h2>', 
                       unsafe_allow_html=True)
            
            st.markdown("""
            Identify distinct customer segments with similar characteristics and behaviors.
            Use these segments for targeted marketing strategies.
            """)
            
            # Number of clusters selection
            n_clusters = st.slider("Number of Segments", min_value=3, max_value=6, value=4)
            
            with st.spinner("Performing customer segmentation..."):
                segmenter = run_customer_segmentation(df, n_clusters=n_clusters)
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Segment Overview", "📈 Characteristics", 
                                              "🗺️ Visualization", "💡 Profiles"])
            
            with tab1:
                st.subheader("Segment Analysis Summary")
                segment_df = segmenter.analyze_segments()
                st.dataframe(segment_df, use_container_width=True)
                
                # Highlight best segment
                best_segment = segment_df.loc[segment_df['Conversion Rate'].str.rstrip('%').astype(float).idxmax(), 'Segment']
                st.success(f"🎯 **Best Performing Segment:** {best_segment}")
            
            with tab2:
                st.subheader("Segment Characteristics")
                fig = segmenter.plot_segment_characteristics()
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("2D Visualization of Segments")
                fig = segmenter.plot_segments_2d()
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 Segments are visualized using PCA (Principal Component Analysis) to reduce dimensionality to 2D")
            
            with tab4:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                profiles = segmenter.get_segment_profiles()
                st.markdown(profiles)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # =====================
        # CONTACT OPTIMIZATION
        # =====================
        elif section == "contact_optimization":
            st.markdown('<h2 class="section-header">📞 Contact Optimization</h2>', 
                       unsafe_allow_html=True)
            
            st.markdown("""
            Optimize campaign effectiveness by understanding:
            - **How many** times to contact customers
            - **When** to contact them (month, day)
            - **How** to contact them (channel)
            """)
            
            with st.spinner("Analyzing contact strategies..."):
                optimizer = run_contact_optimization(df)
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📞 Frequency", "📅 Timing", 
                                              "📱 Channel", "💡 Insights"])
            
            with tab1:
                st.subheader("Contact Frequency Analysis")
                fig = optimizer.plot_contact_frequency_impact()
                st.plotly_chart(fig, use_container_width=True)
                
                freq_df = optimizer.analyze_contact_frequency()
                st.dataframe(freq_df.head(10), use_container_width=True)
            
            with tab2:
                st.subheader("Optimal Timing Analysis")
                fig = optimizer.plot_timing_analysis()
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Contact Channel")
                    fig = optimizer.plot_channel_analysis()
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Previous Campaign Impact")
                    fig = optimizer.plot_previous_outcome_impact()
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                insights = optimizer.get_optimization_insights()
                st.markdown(insights)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # =====================
        # ECONOMIC IMPACT
        # =====================
        elif section == "economic_impact":
            st.markdown('<h2 class="section-header">💰 Economic Impact Analysis</h2>', 
                       unsafe_allow_html=True)
            
            st.markdown("""
            Understand how macroeconomic factors influence campaign success:
            - Employment rates
            - Consumer confidence
            - Interest rates (Euribor)
            - Consumer price index
            """)
            
            with st.spinner("Analyzing economic impacts..."):
                econ_analyzer = run_economic_impact_analysis(df)
            
            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Correlations", "🌍 Conditions", 
                                              "📈 Trends", "💡 Insights"])
            
            with tab1:
                st.subheader("Economic Indicator Correlations")
                fig = econ_analyzer.plot_economic_correlations()
                st.plotly_chart(fig, use_container_width=True)
                
                # Correlation table
                corr_df = econ_analyzer.analyze_economic_correlations()
                st.dataframe(corr_df, use_container_width=True)
            
            with tab2:
                st.subheader("Campaign Success by Economic Conditions")
                fig = econ_analyzer.plot_economic_conditions_impact()
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Economic Indicators Over Time")
                fig = econ_analyzer.plot_indicator_trends_over_time()
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Conversion by Indicator Ranges")
                fig = econ_analyzer.plot_optimal_indicator_ranges()
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                insights = econ_analyzer.get_economic_insights()
                st.markdown(insights)
                st.markdown('</div>', unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("❌ File not found. Please check the file path.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p style='font-size: 1.2rem; font-weight: bold; color: #2c3e50; margin-bottom: 10px;'>Masood Nazari</p>
        <p style='color: #7f8c8d; margin-bottom: 15px;'>Data Science | AI | Clinical Research</p>
        <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 10px;'>
            <a href='mailto:M.Nazari@soton.ac.uk' style='color: #3498db; text-decoration: none;'>✉️ M.Nazari@soton.ac.uk</a>
            <a href='https://michaeltheanalyst.github.io/' target='_blank' style='color: #3498db; text-decoration: none;'>🌐 Portfolio</a>
            <a href='https://www.linkedin.com/in/masood-nazari/' target='_blank' style='color: #3498db; text-decoration: none;'>💼 LinkedIn</a>
            <a href='https://github.com/michaeltheanalyst' target='_blank' style='color: #3498db; text-decoration: none;'>🔗 GitHub</a>
        </div>
        <p style='color: #95a5a6; font-size: 0.9rem; margin-top: 10px;'>Bank Marketing Analytics Dashboard | Built with Streamlit & Plotly | 2025</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


