"""
Economic Impact Analysis Module
Analyze how macroeconomic factors affect campaign success
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class EconomicImpactAnalyzer:
    """Analyze economic indicators' impact on campaign success"""
    
    def __init__(self, df):
        self.df = df
        self.economic_indicators = [
            'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 
            'euribor3m', 'nr.employed'
        ]
        
    def analyze_economic_correlations(self):
        """Analyze correlation between economic indicators and conversion"""
        correlations = []
        
        for indicator in self.economic_indicators:
            corr, pvalue = stats.pearsonr(self.df[indicator], self.df['y_binary'])
            correlations.append({
                'Indicator': indicator,
                'Correlation': corr,
                'P-Value': pvalue,
                'Significant': 'Yes' if pvalue < 0.05 else 'No'
            })
        
        corr_df = pd.DataFrame(correlations)
        corr_df = corr_df.sort_values('Correlation', ascending=False, key=abs)
        
        return corr_df
    
    def plot_economic_correlations(self):
        """Plot correlations between economic indicators and conversion"""
        corr_df = self.analyze_economic_correlations()
        
        # Clean indicator names for display
        display_names = {
            'emp.var.rate': 'Employment Var. Rate',
            'cons.price.idx': 'Consumer Price Index',
            'cons.conf.idx': 'Consumer Confidence',
            'euribor3m': 'Euribor 3M Rate',
            'nr.employed': 'Number Employed'
        }
        
        corr_df['Indicator_Display'] = corr_df['Indicator'].map(display_names)
        
        # Color by positive/negative
        colors = ['red' if x < 0 else 'green' for x in corr_df['Correlation']]
        
        fig = go.Figure(data=[
            go.Bar(
                y=corr_df['Indicator_Display'],
                x=corr_df['Correlation'],
                orientation='h',
                marker=dict(color=colors),
                text=corr_df['Correlation'].round(3),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title='Economic Indicators Correlation with Conversion',
            xaxis_title='Correlation Coefficient',
            yaxis_title='Economic Indicator',
            template='plotly_white',
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        # Add vertical line at 0
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        
        return fig
    
    def analyze_economic_conditions_segments(self):
        """Segment conversion by economic conditions"""
        # Create economic condition categories based on key indicators
        self.df['economic_condition'] = 'Neutral'
        
        # High confidence + low unemployment + low interest rate = Good
        good_conditions = (
            (self.df['cons.conf.idx'] > self.df['cons.conf.idx'].median()) &
            (self.df['euribor3m'] < self.df['euribor3m'].median()) &
            (self.df['emp.var.rate'] > self.df['emp.var.rate'].median())
        )
        
        # Opposite = Bad
        bad_conditions = (
            (self.df['cons.conf.idx'] < self.df['cons.conf.idx'].quantile(0.25)) &
            (self.df['euribor3m'] > self.df['euribor3m'].quantile(0.75))
        )
        
        self.df.loc[good_conditions, 'economic_condition'] = 'Favorable'
        self.df.loc[bad_conditions, 'economic_condition'] = 'Unfavorable'
        
        # Analyze conversion by condition
        econ_analysis = self.df.groupby('economic_condition').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        
        econ_analysis.columns = ['condition', 'conversions', 'total', 'conversion_rate']
        econ_analysis['conversion_rate_pct'] = econ_analysis['conversion_rate'] * 100
        
        return econ_analysis
    
    def plot_economic_conditions_impact(self):
        """Plot impact of economic conditions on conversion"""
        econ_analysis = self.analyze_economic_conditions_segments()
        
        # Order categories
        order = ['Unfavorable', 'Neutral', 'Favorable']
        econ_analysis['condition'] = pd.Categorical(econ_analysis['condition'], 
                                                    categories=order, ordered=True)
        econ_analysis = econ_analysis.sort_values('condition')
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Conversion Rate by Economic Condition', 'Sample Distribution'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}]]
        )
        
        # Conversion rate
        colors_map = {'Unfavorable': '#FF6B6B', 'Neutral': '#FFD93D', 'Favorable': '#6BCF7F'}
        colors = [colors_map[c] for c in econ_analysis['condition']]
        
        fig.add_trace(
            go.Bar(
                x=econ_analysis['condition'],
                y=econ_analysis['conversion_rate_pct'],
                marker_color=colors,
                text=econ_analysis['conversion_rate_pct'].round(1),
                texttemplate='%{text}%',
                textposition='auto',
                name='Conversion Rate'
            ),
            row=1, col=1
        )
        
        # Distribution
        fig.add_trace(
            go.Pie(
                labels=econ_analysis['condition'],
                values=econ_analysis['total'],
                marker=dict(colors=colors),
                name='Distribution'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Economic Condition", row=1, col=1)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        
        fig.update_layout(
            title_text="Campaign Success by Economic Conditions",
            showlegend=False,
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def plot_indicator_trends_over_time(self):
        """Plot how economic indicators vary over campaign timeline"""
        # Aggregate by month
        month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        
        # Get unique month-indicator combinations
        monthly_data = self.df.groupby('month')[self.economic_indicators + ['y_binary']].mean().reset_index()
        monthly_data['month'] = pd.Categorical(monthly_data['month'], 
                                              categories=month_order, ordered=True)
        monthly_data = monthly_data.sort_values('month')
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Employment Var. Rate', 'Consumer Price Index',
                'Consumer Confidence', 'Euribor 3M Rate',
                'Number Employed', 'Conversion Rate'
            )
        )
        
        indicators_plot = [
            ('emp.var.rate', 1, 1),
            ('cons.price.idx', 1, 2),
            ('cons.conf.idx', 2, 1),
            ('euribor3m', 2, 2),
            ('nr.employed', 3, 1),
            ('y_binary', 3, 2)
        ]
        
        for indicator, row, col in indicators_plot:
            fig.add_trace(
                go.Scatter(
                    x=monthly_data['month'],
                    y=monthly_data[indicator] if indicator != 'y_binary' else monthly_data[indicator] * 100,
                    mode='lines+markers',
                    name=indicator,
                    line=dict(width=2),
                    marker=dict(size=8),
                    showlegend=False
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title_text="Economic Indicators Over Campaign Timeline",
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def analyze_indicator_ranges(self):
        """Analyze optimal ranges for each economic indicator"""
        ranges_analysis = []
        
        for indicator in self.economic_indicators:
            try:
                # Create quartiles without labels first to handle duplicates
                quartiles = pd.qcut(self.df[indicator], q=4, duplicates='drop')
                
                # Convert to string representation for grouping
                quartiles_str = quartiles.astype(str)
                
                quartile_conv = self.df.groupby(quartiles_str, observed=False)['y_binary'].agg(['mean', 'count']).reset_index()
                quartile_conv.columns = ['Range', 'Conversion_Rate', 'Count']
                quartile_conv['Indicator'] = indicator
                quartile_conv['Conversion_Rate_Pct'] = quartile_conv['Conversion_Rate'] * 100
                
                ranges_analysis.append(quartile_conv)
            except Exception as e:
                # If qcut fails (e.g., too few unique values), use simple binning
                print(f"Warning: Could not create quartiles for {indicator}, using simple bins")
                try:
                    quartiles = pd.cut(self.df[indicator], bins=4, duplicates='drop')
                    quartiles_str = quartiles.astype(str)
                    
                    quartile_conv = self.df.groupby(quartiles_str, observed=False)['y_binary'].agg(['mean', 'count']).reset_index()
                    quartile_conv.columns = ['Range', 'Conversion_Rate', 'Count']
                    quartile_conv['Indicator'] = indicator
                    quartile_conv['Conversion_Rate_Pct'] = quartile_conv['Conversion_Rate'] * 100
                    
                    ranges_analysis.append(quartile_conv)
                except:
                    # Skip this indicator if it still fails
                    continue
        
        if ranges_analysis:
            return pd.concat(ranges_analysis, ignore_index=True)
        else:
            # Return empty dataframe with correct structure if all failed
            return pd.DataFrame(columns=['Range', 'Conversion_Rate', 'Count', 'Indicator', 'Conversion_Rate_Pct'])
    
    def plot_optimal_indicator_ranges(self):
        """Plot optimal ranges for economic indicators"""
        ranges_df = self.analyze_indicator_ranges()
        
        # Clean indicator names
        display_names = {
            'emp.var.rate': 'Employment Var. Rate',
            'cons.price.idx': 'Consumer Price Index',
            'cons.conf.idx': 'Consumer Confidence',
            'euribor3m': 'Euribor 3M Rate',
            'nr.employed': 'Number Employed'
        }
        ranges_df['Indicator_Display'] = ranges_df['Indicator'].map(display_names)
        
        fig = px.bar(
            ranges_df,
            x='Range',
            y='Conversion_Rate_Pct',
            color='Indicator_Display',
            barmode='group',
            title='Conversion Rate by Economic Indicator Ranges',
            labels={
                'Range': 'Indicator Range (Quartile)',
                'Conversion_Rate_Pct': 'Conversion Rate (%)',
                'Indicator_Display': 'Economic Indicator'
            },
            template='plotly_white',
            height=500
        )
        
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def get_economic_insights(self):
        """Generate actionable economic insights"""
        corr_df = self.analyze_economic_correlations()
        econ_analysis = self.analyze_economic_conditions_segments()
        
        insights = []
        insights.append("### 📈 Economic Impact Insights\n")
        
        # Top correlations
        top_positive = corr_df[corr_df['Correlation'] > 0].iloc[0] if any(corr_df['Correlation'] > 0) else None
        top_negative = corr_df[corr_df['Correlation'] < 0].iloc[0] if any(corr_df['Correlation'] < 0) else None
        
        insights.append("**🔍 Key Economic Drivers:**\n")
        
        if top_positive is not None:
            insights.append(f"- **Positive Impact:** {top_positive['Indicator'].replace('.', ' ').title()}")
            insights.append(f"  - Correlation: {top_positive['Correlation']:.3f} (p={top_positive['P-Value']:.4f})")
            insights.append(f"  - Higher values → Better conversion rates\n")
        
        if top_negative is not None:
            insights.append(f"- **Negative Impact:** {top_negative['Indicator'].replace('.', ' ').title()}")
            insights.append(f"  - Correlation: {top_negative['Correlation']:.3f} (p={top_negative['P-Value']:.4f})")
            insights.append(f"  - Higher values → Lower conversion rates\n")
        
        # Economic conditions impact
        if len(econ_analysis) >= 2:
            favorable_rate = econ_analysis[econ_analysis['condition'] == 'Favorable']['conversion_rate_pct'].values
            unfavorable_rate = econ_analysis[econ_analysis['condition'] == 'Unfavorable']['conversion_rate_pct'].values
            
            if len(favorable_rate) > 0 and len(unfavorable_rate) > 0:
                rate_diff = favorable_rate[0] - unfavorable_rate[0]
                insights.append(f"**🌍 Economic Conditions Impact:**")
                insights.append(f"- Favorable conditions: {favorable_rate[0]:.1f}% conversion")
                insights.append(f"- Unfavorable conditions: {unfavorable_rate[0]:.1f}% conversion")
                insights.append(f"- **Difference: {rate_diff:.1f} percentage points**\n")
        
        insights.append("**💡 Strategic Recommendations:**")
        insights.append("1. **Monitor economic indicators** - Campaign timing matters")
        insights.append("2. **Scale up campaigns** during favorable economic periods")
        insights.append("3. **Adjust targeting** - Different segments respond differently to economic conditions")
        insights.append("4. **Budget allocation** - Reserve more budget for favorable economic windows")
        insights.append("5. **Message adaptation** - Tailor messaging to current economic sentiment")
        
        return "\n".join(insights)


def run_economic_impact_analysis(df):
    """Run complete economic impact analysis"""
    analyzer = EconomicImpactAnalyzer(df)
    return analyzer


if __name__ == "__main__":
    print("Economic Impact Analysis Module - Run via dashboard")


