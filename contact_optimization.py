"""
Contact Optimization Analysis Module
Analyze optimal contact frequency, timing, and channel
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


class ContactOptimizer:
    """Analyze and optimize contact strategy"""
    
    def __init__(self, df):
        self.df = df
        
    def analyze_contact_frequency(self):
        """Analyze optimal number of contacts"""
        freq_analysis = self.df.groupby('campaign').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        
        freq_analysis.columns = ['campaign', 'conversions', 'total_contacts', 'conversion_rate']
        freq_analysis['conversion_rate_pct'] = freq_analysis['conversion_rate'] * 100
        
        return freq_analysis
    
    def plot_contact_frequency_impact(self):
        """Plot relationship between contact frequency and conversion"""
        freq_analysis = self.analyze_contact_frequency()
        
        # Limit to reasonable number of contacts for visualization
        freq_analysis_plot = freq_analysis[freq_analysis['campaign'] <= 10]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Conversion Rate by Contact Frequency', 'Number of Customers by Contact Frequency'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Conversion rate
        fig.add_trace(
            go.Scatter(
                x=freq_analysis_plot['campaign'],
                y=freq_analysis_plot['conversion_rate_pct'],
                mode='lines+markers',
                name='Conversion Rate %',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ),
            row=1, col=1
        )
        
        # Customer count
        fig.add_trace(
            go.Bar(
                x=freq_analysis_plot['campaign'],
                y=freq_analysis_plot['total_contacts'],
                name='Number of Customers',
                marker_color='lightblue'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Number of Contacts", row=1, col=1)
        fig.update_xaxes(title_text="Number of Contacts", row=1, col=2)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Number of Customers", row=1, col=2)
        
        fig.update_layout(
            title_text="Contact Frequency Analysis",
            showlegend=False,
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def analyze_contact_timing(self):
        """Analyze optimal month and day for contact"""
        # By month
        month_analysis = self.df.groupby('month').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        month_analysis.columns = ['month', 'conversions', 'total', 'conversion_rate']
        month_analysis['conversion_rate_pct'] = month_analysis['conversion_rate'] * 100
        
        # By day of week
        day_analysis = self.df.groupby('day_of_week').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        day_analysis.columns = ['day_of_week', 'conversions', 'total', 'conversion_rate']
        day_analysis['conversion_rate_pct'] = day_analysis['conversion_rate'] * 100
        
        return month_analysis, day_analysis
    
    def plot_timing_analysis(self):
        """Plot timing analysis (month and day)"""
        month_analysis, day_analysis = self.analyze_contact_timing()
        
        # Order months
        month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month_analysis['month'] = pd.Categorical(month_analysis['month'], 
                                                 categories=month_order, ordered=True)
        month_analysis = month_analysis.sort_values('month')
        
        # Order days
        day_order = ['mon', 'tue', 'wed', 'thu', 'fri']
        day_analysis['day_of_week'] = pd.Categorical(day_analysis['day_of_week'],
                                                     categories=day_order, ordered=True)
        day_analysis = day_analysis.sort_values('day_of_week')
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Conversion Rate by Month', 'Conversion Rate by Day of Week'),
            specs=[[{'secondary_y': True}], [{'secondary_y': True}]]
        )
        
        # Month analysis
        fig.add_trace(
            go.Bar(
                x=month_analysis['month'],
                y=month_analysis['total'],
                name='Total Contacts',
                marker_color='lightblue',
                opacity=0.6
            ),
            row=1, col=1,
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=month_analysis['month'],
                y=month_analysis['conversion_rate_pct'],
                name='Conversion Rate %',
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=10)
            ),
            row=1, col=1,
            secondary_y=True
        )
        
        # Day analysis
        fig.add_trace(
            go.Bar(
                x=day_analysis['day_of_week'],
                y=day_analysis['total'],
                name='Total Contacts',
                marker_color='lightgreen',
                opacity=0.6,
                showlegend=False
            ),
            row=2, col=1,
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=day_analysis['day_of_week'],
                y=day_analysis['conversion_rate_pct'],
                name='Conversion Rate %',
                mode='lines+markers',
                line=dict(color='darkgreen', width=3),
                marker=dict(size=10),
                showlegend=False
            ),
            row=2, col=1,
            secondary_y=True
        )
        
        # Update axes
        fig.update_xaxes(title_text="Month", row=1, col=1)
        fig.update_xaxes(title_text="Day of Week", row=2, col=1)
        fig.update_yaxes(title_text="Total Contacts", row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Total Contacts", row=2, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=2, col=1, secondary_y=True)
        
        fig.update_layout(
            title_text="Contact Timing Optimization",
            height=700,
            template='plotly_white'
        )
        
        return fig
    
    def analyze_contact_channel(self):
        """Analyze cellular vs telephone effectiveness"""
        channel_analysis = self.df.groupby('contact').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        
        channel_analysis.columns = ['contact', 'conversions', 'total', 'conversion_rate']
        channel_analysis['conversion_rate_pct'] = channel_analysis['conversion_rate'] * 100
        
        return channel_analysis
    
    def plot_channel_analysis(self):
        """Plot contact channel effectiveness"""
        channel_analysis = self.analyze_contact_channel()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Conversion Rate by Channel', 'Volume by Channel'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}]]
        )
        
        # Conversion rate comparison
        fig.add_trace(
            go.Bar(
                x=channel_analysis['contact'],
                y=channel_analysis['conversion_rate_pct'],
                text=channel_analysis['conversion_rate_pct'].round(1),
                texttemplate='%{text}%',
                textposition='auto',
                marker_color=['#FF6B6B', '#4ECDC4'],
                name='Conversion Rate'
            ),
            row=1, col=1
        )
        
        # Volume distribution
        fig.add_trace(
            go.Pie(
                labels=channel_analysis['contact'],
                values=channel_analysis['total'],
                name='Volume',
                marker=dict(colors=['#FF6B6B', '#4ECDC4'])
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Contact Channel", row=1, col=1)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
        
        fig.update_layout(
            title_text="Contact Channel Analysis",
            showlegend=False,
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def analyze_previous_outcome_impact(self):
        """Analyze impact of previous campaign outcome"""
        outcome_analysis = self.df.groupby('poutcome').agg({
            'y_binary': ['sum', 'count', 'mean']
        }).reset_index()
        
        outcome_analysis.columns = ['poutcome', 'conversions', 'total', 'conversion_rate']
        outcome_analysis['conversion_rate_pct'] = outcome_analysis['conversion_rate'] * 100
        
        return outcome_analysis
    
    def plot_previous_outcome_impact(self):
        """Plot impact of previous campaign outcome"""
        outcome_analysis = self.analyze_previous_outcome_impact()
        
        fig = go.Figure(data=[
            go.Bar(
                x=outcome_analysis['poutcome'],
                y=outcome_analysis['conversion_rate_pct'],
                text=outcome_analysis['conversion_rate_pct'].round(1),
                texttemplate='%{text}%',
                textposition='auto',
                marker=dict(
                    color=outcome_analysis['conversion_rate_pct'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Conv. Rate %")
                )
            )
        ])
        
        # Add sample sizes as annotation
        for i, row in outcome_analysis.iterrows():
            fig.add_annotation(
                x=row['poutcome'],
                y=row['conversion_rate_pct'] / 2,
                text=f"n={row['total']:,}",
                showarrow=False,
                font=dict(size=10, color='white')
            )
        
        fig.update_layout(
            title='Impact of Previous Campaign Outcome on Current Conversion',
            xaxis_title='Previous Campaign Outcome',
            yaxis_title='Conversion Rate (%)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def get_optimization_insights(self):
        """Generate actionable optimization insights"""
        freq_analysis = self.analyze_contact_frequency()
        month_analysis, day_analysis = self.analyze_contact_timing()
        channel_analysis = self.analyze_contact_channel()
        outcome_analysis = self.analyze_previous_outcome_impact()
        
        insights = []
        insights.append("### 🎯 Contact Optimization Insights\n")
        
        # Frequency insights
        optimal_contacts = freq_analysis[freq_analysis['conversion_rate'] == freq_analysis['conversion_rate'].max()]['campaign'].values[0]
        insights.append(f"**📞 Optimal Contact Frequency:** {int(optimal_contacts)} contact(s)")
        
        # Check for diminishing returns
        if len(freq_analysis) > 3:
            early_conv = freq_analysis[freq_analysis['campaign'] <= 2]['conversion_rate'].mean()
            late_conv = freq_analysis[freq_analysis['campaign'] > 5]['conversion_rate'].mean()
            if late_conv < early_conv * 0.5:
                insights.append(f"- ⚠️ **Campaign Fatigue Detected:** Conversion drops by {(1-late_conv/early_conv)*100:.0f}% after 5+ contacts")
        
        # Best month
        month_analysis_sorted = month_analysis.sort_values('conversion_rate', ascending=False)
        best_month = month_analysis_sorted.iloc[0]['month']
        best_month_rate = month_analysis_sorted.iloc[0]['conversion_rate_pct']
        insights.append(f"\n**📅 Best Month:** {best_month.capitalize()} ({best_month_rate:.1f}% conversion rate)")
        
        # Best day
        day_analysis_sorted = day_analysis.sort_values('conversion_rate', ascending=False)
        best_day = day_analysis_sorted.iloc[0]['day_of_week']
        best_day_rate = day_analysis_sorted.iloc[0]['conversion_rate_pct']
        insights.append(f"**📆 Best Day:** {best_day.capitalize()} ({best_day_rate:.1f}% conversion rate)")
        
        # Best channel
        channel_sorted = channel_analysis.sort_values('conversion_rate', ascending=False)
        best_channel = channel_sorted.iloc[0]['contact']
        best_channel_rate = channel_sorted.iloc[0]['conversion_rate_pct']
        channel_lift = (channel_sorted.iloc[0]['conversion_rate'] / channel_sorted.iloc[1]['conversion_rate'] - 1) * 100
        insights.append(f"\n**📱 Recommended Channel:** {best_channel.capitalize()} ({best_channel_rate:.1f}% conversion)")
        insights.append(f"- {channel_lift:.0f}% better than alternative channel")
        
        # Previous outcome impact
        if 'success' in outcome_analysis['poutcome'].values:
            prev_success_rate = outcome_analysis[outcome_analysis['poutcome'] == 'success']['conversion_rate_pct'].values[0]
            insights.append(f"\n**🔄 Re-engagement Strategy:**")
            insights.append(f"- Previous success → {prev_success_rate:.1f}% current conversion")
            insights.append(f"- **Recommendation:** Prioritize customers with previous successful engagements")
        
        insights.append("\n**💡 Action Items:**")
        insights.append(f"1. Limit campaigns to {int(optimal_contacts)}-3 contacts maximum")
        insights.append(f"2. Focus campaigns during {best_month.capitalize()}")
        insights.append(f"3. Prioritize {best_channel.capitalize()} as primary channel")
        insights.append(f"4. Target {best_day.capitalize()} for initial contacts")
        insights.append(f"5. Create separate strategy for previous responders")
        
        return "\n".join(insights)


def run_contact_optimization(df):
    """Run complete contact optimization analysis"""
    optimizer = ContactOptimizer(df)
    return optimizer


if __name__ == "__main__":
    print("Contact Optimization Module - Run via dashboard")


