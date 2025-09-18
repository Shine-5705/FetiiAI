import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any
from data_processor import DataProcessor

def create_visualizations(data_processor: DataProcessor) -> Dict[str, Any]:
    """
    Create all visualizations for the Fetii dashboard.
    """
    insights = data_processor.get_quick_insights()
    df = data_processor.df
    
    visualizations = {}
    
    visualizations['hourly_distribution'] = create_hourly_chart(insights['hourly_distribution'])
    
    visualizations['group_size_distribution'] = create_group_size_chart(insights['group_size_distribution'])
    
    visualizations['popular_locations'] = create_locations_chart(insights['top_pickups'])
    
    visualizations['time_heatmap'] = create_time_heatmap(df)
    
    visualizations['daily_volume'] = create_daily_volume_chart(df)
    
    return visualizations

def create_hourly_chart(hourly_data: Dict[int, int]) -> go.Figure:
    """Create hourly distribution chart."""
    hours = list(hourly_data.keys())
    counts = list(hourly_data.values())
    
    hour_labels = []
    for hour in hours:
        if hour == 0:
            hour_labels.append("12 AM")
        elif hour < 12:
            hour_labels.append(f"{hour} AM")
        elif hour == 12:
            hour_labels.append("12 PM")
        else:
            hour_labels.append(f"{hour-12} PM")
    
    fig = go.Figure()
    
    colors = []
    max_count = max(counts)
    for count in counts:
        intensity = count / max_count
        if intensity > 0.8:
            colors.append(f'rgba(255, 69, 0, {0.7 + intensity * 0.3})')  # Red-orange for peak
        elif intensity > 0.5:
            colors.append(f'rgba(255, 140, 0, {0.6 + intensity * 0.4})')  # Orange
        else:
            colors.append(f'rgba(102, 126, 234, {0.4 + intensity * 0.4})')  # Blue for low
    
    fig.add_trace(go.Bar(
        x=hour_labels,
        y=counts,
        marker_color=colors,
        name='Trips',
        hovertemplate='<b>%{x}</b><br>Trips: %{y}<extra></extra>',
        text=counts,
        textposition='outside'
    ))
    
    fig.update_layout(
        title={
            'text': '🕒 Trip Distribution by Hour',
            'x': 0.5,
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        xaxis_title='Hour of Day',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        height=300,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_group_size_chart(group_data: Dict[int, int]) -> go.Figure:
    """Create group size distribution chart."""
    sizes = list(group_data.keys())
    counts = list(group_data.values())
    
    colors = px.colors.qualitative.Set3[:len(sizes)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=[f"{size} passengers" for size in sizes],
        values=counts,
        marker_colors=colors,
        hovertemplate='<b>%{label}</b><br>Trips: %{value}<br>Percentage: %{percent}<extra></extra>',
        textinfo='label+percent',
        textposition='auto',
        hole=0.4 
    ))
    
    fig.update_layout(
        title={
            'text': '👥 Group Size Distribution',
            'x': 0.5,
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        height=300,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    
    return fig

def create_locations_chart(pickup_data: list) -> go.Figure:
    """Create popular locations chart."""
    locations = [item[0] for item in pickup_data[:8]]
    counts = [item[1] for item in pickup_data[:8]]
    
    fig = go.Figure()
    
    colors = []
    max_count = max(counts)
    for count in counts:
        intensity = count / max_count
        colors.append(f'rgba(102, 126, 234, {0.5 + intensity * 0.5})')
    
    fig.add_trace(go.Bar(
        x=counts,
        y=locations,
        orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>Pickups: %{x}<extra></extra>',
        text=counts,
        textposition='outside'
    ))
    
    fig.update_layout(
        title={
            'text': '📍 Top Pickup Locations',
            'x': 0.5,
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        xaxis_title='Number of Pickups',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        height=300,
        margin=dict(t=50, b=50, l=120, r=50)
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_time_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create time-based heatmap."""
    df_copy = df.copy()
    df_copy['day_num'] = df_copy['datetime'].dt.dayofweek
    df_copy['day_name'] = df_copy['datetime'].dt.day_name()
    
    heatmap_data = df_copy.groupby(['day_num', 'hour']).size().reset_index(name='trips')
    heatmap_pivot = heatmap_data.pivot(index='day_num', columns='hour', values='trips').fillna(0)
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    hour_labels = []
    for hour in range(24):
        if hour == 0:
            hour_labels.append("12 AM")
        elif hour < 12:
            hour_labels.append(f"{hour} AM")
        elif hour == 12:
            hour_labels.append("12 PM")
        else:
            hour_labels.append(f"{hour-12} PM")
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=heatmap_pivot.values,
        x=hour_labels,
        y=day_names,
        colorscale='Viridis',
        hovertemplate='<b>%{y}</b><br>%{x}<br>Trips: %{z}<extra></extra>',
        colorbar=dict(title="Trips")
    ))
    
    fig.update_layout(
        title={
            'text': '🗓️ Trip Patterns by Day & Hour',
            'x': 0.5,
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        height=400,
        margin=dict(t=50, b=50, l=100, r=50)
    )
    
    return fig

def create_daily_volume_chart(df: pd.DataFrame) -> go.Figure:
    """Create daily trip volume chart."""
    daily_trips = df.groupby('date').size().reset_index(name='trips')
    daily_trips['date'] = pd.to_datetime(daily_trips['date'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_trips['date'],
        y=daily_trips['trips'],
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Trips: %{y}<extra></extra>',
        name='Daily Trips'
    ))
    
    z = np.polyfit(range(len(daily_trips)), daily_trips['trips'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=daily_trips['date'],
        y=p(range(len(daily_trips))),
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Trend',
        hovertemplate='Trend: %{y:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '📅 Daily Trip Volume',
            'x': 0.5,
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        xaxis_title='Date',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        height=300,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=True,
        legend=dict(x=0.02, y=0.98)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_advanced_analytics_charts(data_processor: DataProcessor) -> Dict[str, Any]:
    """Create advanced analytics visualizations."""
    df = data_processor.df
    charts = {}
    
    if all(col in df.columns for col in ['Pick Up Latitude', 'Pick Up Longitude', 'Drop Off Latitude', 'Drop Off Longitude']):
        charts['distance_analysis'] = create_distance_analysis(df)
    
    charts['peak_hours_by_group'] = create_peak_hours_by_group(df)
    
    charts['location_network'] = create_location_flow(df)
    
    return charts

def create_distance_analysis(df: pd.DataFrame) -> go.Figure:
    """Create group size vs trip distance analysis."""
    df_copy = df.copy()
    df_copy['distance'] = np.sqrt(
        (df_copy['Drop Off Latitude'] - df_copy['Pick Up Latitude'])**2 + 
        (df_copy['Drop Off Longitude'] - df_copy['Pick Up Longitude'])**2
    ) * 111
    
    distance_by_group = df_copy.groupby('Total Passengers')['distance'].agg(['mean', 'std', 'count']).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=distance_by_group['Total Passengers'],
        y=distance_by_group['mean'],
        mode='markers+lines',
        marker=dict(size=distance_by_group['count']/10, color='#667eea'),
        line=dict(color='#667eea', width=2),
        error_y=dict(type='data', array=distance_by_group['std']),
        hovertemplate='<b>Group Size: %{x}</b><br>Avg Distance: %{y:.2f} km<br>Trips: %{marker.size}<extra></extra>',
        name='Average Distance'
    ))
    
    fig.update_layout(
        title='🗺️ Average Trip Distance by Group Size',
        xaxis_title='Group Size (Passengers)',
        yaxis_title='Average Distance (km)',
        height=400
    )
    
    return fig

def create_peak_hours_by_group(df: pd.DataFrame) -> go.Figure:
    """Create peak hours analysis by group size category."""
    df_copy = df.copy()
    df_copy['group_category'] = df_copy['Total Passengers'].apply(
        lambda x: 'Small (1-4)' if x <= 4 else
                  'Medium (5-8)' if x <= 8 else
                  'Large (9-12)' if x <= 12 else
                  'Extra Large (13+)'
    )
    
    hourly_by_group = df_copy.groupby(['group_category', 'hour']).size().reset_index(name='trips')
    
    fig = go.Figure()
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    categories = hourly_by_group['group_category'].unique()
    
    for i, category in enumerate(categories):
        data = hourly_by_group[hourly_by_group['group_category'] == category]
        fig.add_trace(go.Scatter(
            x=data['hour'],
            y=data['trips'],
            mode='lines+markers',
            name=category,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='⏰ Peak Hours by Group Size Category',
        xaxis_title='Hour of Day',
        yaxis_title='Number of Trips',
        height=400,
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig

def create_location_flow(df: pd.DataFrame) -> go.Figure:
    """Create location flow/network visualization."""
    flow_data = df.groupby(['pickup_main', 'dropoff_main']).size().reset_index(name='trips')
    flow_data = flow_data.sort_values('trips', ascending=False).head(20)
    
    all_locations = list(set(flow_data['pickup_main'].tolist() + flow_data['dropoff_main'].tolist()))
    location_map = {loc: i for i, loc in enumerate(all_locations)}
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_locations,
            color="#667eea"
        ),
        link=dict(
            source=[location_map[loc] for loc in flow_data['pickup_main']],
            target=[location_map[loc] for loc in flow_data['dropoff_main']],
            value=flow_data['trips'].tolist(),
            color="rgba(102, 126, 234, 0.3)"
        )
    )])
    
    fig.update_layout(
        title="🔄 Top Location Flow Patterns",
        font_size=10,
        height=500
    )
    
    return fig