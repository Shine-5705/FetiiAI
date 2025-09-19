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
    
    # Core visualizations
    visualizations['hourly_distribution'] = create_hourly_chart(insights['hourly_distribution'])
    visualizations['group_size_distribution'] = create_group_size_chart(insights['group_size_distribution'])
    visualizations['popular_locations'] = create_locations_chart(insights['top_pickups'])
    
    # Advanced visualizations
    visualizations['time_heatmap'] = create_time_heatmap(df)
    visualizations['daily_volume'] = create_daily_volume_chart(df)
    visualizations['trip_distance_analysis'] = create_distance_analysis(df)
    visualizations['location_comparison'] = create_location_comparison(df)
    visualizations['peak_patterns'] = create_peak_patterns(df)
    
    return visualizations

def create_hourly_chart(hourly_data: Dict[int, int]) -> go.Figure:
    """Create modern hourly distribution chart."""
    hours = sorted(hourly_data.keys())
    counts = [hourly_data[hour] for hour in hours]
    
    # Create hour labels
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
    
    # Create gradient colors based on intensity
    max_count = max(counts)
    colors = []
    for count in counts:
        intensity = count / max_count
        if intensity > 0.8:
            colors.append('#dc2626')  # Red for peak
        elif intensity > 0.6:
            colors.append('#ea580c')  # Orange-red
        elif intensity > 0.4:
            colors.append('#d97706')  # Orange
        elif intensity > 0.2:
            colors.append('#3b82f6')  # Blue
        else:
            colors.append('#6b7280')  # Gray for low activity
    
    fig.add_trace(go.Bar(
        x=hour_labels,
        y=counts,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.8)', width=1)
        ),
        name='Trips',
        hovertemplate='<b>%{x}</b><br>Trips: %{y}<extra></extra>',
        text=counts,
        textposition='outside',
        textfont=dict(color='#374151', size=10, family='Inter')
    ))
    
    fig.update_layout(
        title={
            'text': 'Trip Distribution by Hour',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Hour of Day',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=320,
        margin=dict(t=60, b=50, l=50, r=50),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)',
            showline=True,
            linecolor='rgba(156, 163, 175, 0.3)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)',
            showline=True,
            linecolor='rgba(156, 163, 175, 0.3)'
        )
    )
    
    return fig

def create_group_size_chart(group_data: Dict[int, int]) -> go.Figure:
    """Create modern group size distribution chart."""
    sizes = list(group_data.keys())
    counts = list(group_data.values())
    
    # Modern color palette
    colors = [
        '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
        '#8b5cf6', '#06b6d4', '#84cc16', '#f97316',
        '#ec4899', '#6366f1', '#14b8a6', '#eab308'
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=[f"{size} passengers" for size in sizes],
        values=counts,
        marker=dict(
            colors=colors[:len(sizes)],
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Trips: %{value}<br>Percentage: %{percent}<extra></extra>',
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(color='white', size=11, family='Inter'),
        hole=0.4
    ))
    
    fig.update_layout(
        title={
            'text': 'Group Size Distribution',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=320,
        margin=dict(t=60, b=50, l=50, r=50),
        showlegend=False
    )
    
    return fig

def create_locations_chart(pickup_data: list) -> go.Figure:
    """Create modern popular locations chart."""
    locations = [item[0] for item in pickup_data[:8]]
    counts = [item[1] for item in pickup_data[:8]]
    
    # Truncate long location names
    truncated_locations = []
    for loc in locations:
        if len(loc) > 20:
            truncated_locations.append(loc[:17] + "...")
        else:
            truncated_locations.append(loc)
    
    fig = go.Figure()
    
    # Gradient colors
    max_count = max(counts)
    colors = []
    for count in counts:
        intensity = count / max_count
        colors.append(f'rgba(59, 130, 246, {0.4 + intensity * 0.6})')
    
    fig.add_trace(go.Bar(
        x=counts,
        y=truncated_locations,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.8)', width=1),
            cornerradius=4
        ),
        hovertemplate='<b>%{customdata}</b><br>Pickups: %{x}<extra></extra>',
        customdata=locations,
        text=counts,
        textposition='outside',
        textfont=dict(color='#374151', size=10, family='Inter')
    ))
    
    fig.update_layout(
        title={
            'text': 'Top Pickup Locations',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Number of Pickups',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=320,
        margin=dict(t=60, b=50, l=140, r=50),
        yaxis=dict(
            autorange="reversed",
            showline=True,
            linecolor='rgba(156, 163, 175, 0.3)'
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)',
            showline=True,
            linecolor='rgba(156, 163, 175, 0.3)'
        )
    )
    
    return fig

def create_time_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create advanced time-based heatmap."""
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
        colorscale=[
            [0, '#f8fafc'],
            [0.2, '#e2e8f0'],
            [0.4, '#94a3b8'],
            [0.6, '#3b82f6'],
            [0.8, '#1d4ed8'],
            [1, '#1e40af']
        ],
        hovertemplate='<b>%{y}</b><br>%{x}<br>Trips: %{z}<extra></extra>',
        colorbar=dict(
            title=dict(text="Trips", font=dict(family='Inter', color='#374151')),
            tickfont=dict(family='Inter', color='#374151')
        )
    ))
    
    fig.update_layout(
        title={
            'text': 'Trip Patterns by Day & Hour',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=400,
        margin=dict(t=60, b=50, l=100, r=50)
    )
    
    return fig

def create_daily_volume_chart(df: pd.DataFrame) -> go.Figure:
    """Create modern daily trip volume chart."""
    daily_trips = df.groupby('date').size().reset_index(name='trips')
    daily_trips['date'] = pd.to_datetime(daily_trips['date'])
    daily_trips = daily_trips.sort_values('date')
    
    fig = go.Figure()
    
    # Main line
    fig.add_trace(go.Scatter(
        x=daily_trips['date'],
        y=daily_trips['trips'],
        mode='lines+markers',
        line=dict(color='#3b82f6', width=3, shape='spline'),
        marker=dict(size=6, color='#1d4ed8', line=dict(color='white', width=1)),
        fill='tonexty',
        fillcolor='rgba(59, 130, 246, 0.1)',
        hovertemplate='<b>%{x}</b><br>Trips: %{y}<extra></extra>',
        name='Daily Trips'
    ))
    
    # Add trend line
    if len(daily_trips) > 1:
        z = np.polyfit(range(len(daily_trips)), daily_trips['trips'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=daily_trips['date'],
            y=p(range(len(daily_trips))),
            mode='lines',
            line=dict(color='#ef4444', width=2, dash='dot'),
            name='Trend',
            hovertemplate='Trend: %{y:.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': 'Daily Trip Volume',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Date',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=320,
        margin=dict(t=60, b=50, l=50, r=50),
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(156, 163, 175, 0.3)',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)'
        )
    )
    
    return fig

def create_distance_analysis(df: pd.DataFrame) -> go.Figure:
    """Create group size vs trip distance analysis."""
    if not all(col in df.columns for col in ['Pick Up Latitude', 'Pick Up Longitude', 'Drop Off Latitude', 'Drop Off Longitude']):
        return create_placeholder_chart("Distance Analysis", "Location data not available")
    
    df_copy = df.copy()
    df_copy['distance'] = np.sqrt(
        (df_copy['Drop Off Latitude'] - df_copy['Pick Up Latitude'])**2 + 
        (df_copy['Drop Off Longitude'] - df_copy['Pick Up Longitude'])**2
    ) * 111  # Approximate km conversion
    
    distance_by_group = df_copy.groupby('Total Passengers')['distance'].agg(['mean', 'std', 'count']).reset_index()
    distance_by_group = distance_by_group[distance_by_group['count'] >= 3]  # Filter groups with few trips
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=distance_by_group['Total Passengers'],
        y=distance_by_group['mean'],
        mode='markers+lines',
        marker=dict(
            size=distance_by_group['count']/5,
            color=distance_by_group['mean'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Avg Distance (km)"),
            line=dict(color='white', width=1)
        ),
        line=dict(color='#3b82f6', width=2),
        error_y=dict(
            type='data',
            array=distance_by_group['std'],
            color='rgba(59, 130, 246, 0.3)'
        ),
        hovertemplate='<b>Group Size: %{x}</b><br>Avg Distance: %{y:.2f} km<br>Trips: %{marker.size:.0f}<extra></extra>',
        name='Average Distance'
    ))
    
    fig.update_layout(
        title={
            'text': 'Average Trip Distance by Group Size',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Group Size (Passengers)',
        yaxis_title='Average Distance (km)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=400,
        margin=dict(t=60, b=50, l=50, r=50)
    )
    
    return fig

def create_location_comparison(df: pd.DataFrame) -> go.Figure:
    """Create pickup vs dropoff location comparison."""
    pickup_counts = df['pickup_main'].value_counts().head(10)
    dropoff_counts = df['dropoff_main'].value_counts().head(10)
    
    # Get common locations
    common_locations = list(set(pickup_counts.index) & set(dropoff_counts.index))
    if not common_locations:
        # If no common locations, take top 5 from each
        all_locations = list(set(list(pickup_counts.index[:5]) + list(dropoff_counts.index[:5])))
    else:
        all_locations = common_locations[:8]
    
    pickup_values = [pickup_counts.get(loc, 0) for loc in all_locations]
    dropoff_values = [dropoff_counts.get(loc, 0) for loc in all_locations]
    
    # Truncate location names
    truncated_locations = []
    for loc in all_locations:
        if len(loc) > 15:
            truncated_locations.append(loc[:12] + "...")
        else:
            truncated_locations.append(loc)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Pickups',
        x=truncated_locations,
        y=pickup_values,
        marker_color='#3b82f6',
        hovertemplate='<b>%{x}</b><br>Pickups: %{y}<extra></extra>',
        customdata=all_locations
    ))
    
    fig.add_trace(go.Bar(
        name='Drop-offs',
        x=truncated_locations,
        y=dropoff_values,
        marker_color='#10b981',
        hovertemplate='<b>%{x}</b><br>Drop-offs: %{y}<extra></extra>',
        customdata=all_locations
    ))
    
    fig.update_layout(
        title={
            'text': 'Pickup vs Drop-off Comparison',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Locations',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=400,
        margin=dict(t=60, b=50, l=50, r=50),
        barmode='group',
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(156, 163, 175, 0.3)',
            borderwidth=1
        )
    )
    
    return fig

def create_peak_patterns(df: pd.DataFrame) -> go.Figure:
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
    
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
    categories = ['Small (1-4)', 'Medium (5-8)', 'Large (9-12)', 'Extra Large (13+)']
    
    for i, category in enumerate(categories):
        data = hourly_by_group[hourly_by_group['group_category'] == category]
        if not data.empty:
            fig.add_trace(go.Scatter(
                x=data['hour'],
                y=data['trips'],
                mode='lines+markers',
                name=category,
                line=dict(color=colors[i], width=3, shape='spline'),
                marker=dict(size=6, line=dict(color='white', width=1)),
                hovertemplate='<b>%{fullData.name}</b><br>Hour: %{x}<br>Trips: %{y}<extra></extra>'
            ))
    
    fig.update_layout(
        title={
            'text': 'Peak Hours by Group Size Category',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        xaxis_title='Hour of Day',
        yaxis_title='Number of Trips',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        height=400,
        margin=dict(t=60, b=50, l=50, r=50),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(156, 163, 175, 0.3)',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)',
            tickvals=list(range(0, 24, 2)),
            ticktext=[f"{h}:00" for h in range(0, 24, 2)]
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(156, 163, 175, 0.2)'
        )
    )
    
    return fig

def create_placeholder_chart(title: str, message: str) -> go.Figure:
    """Create a placeholder chart when data is not available."""
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16, color='#6b7280', family='Inter')
    )
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(t=60, b=50, l=50, r=50),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    
    return fig