"""
Utility functions for Fetii AI Chatbot
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any, Tuple, Optional
import config

def clean_location_name(location: str) -> str:
    """Clean and standardize location names."""
    if pd.isna(location) or not location:
        return "Unknown"
    
    cleaned = location.strip().title()
    
    suffixes_to_remove = [", Austin, TX", ", Austin, Texas", ", USA", ", United States"]
    for suffix in suffixes_to_remove:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    
    return cleaned

def categorize_location(location: str) -> str:
    """Categorize location type based on keywords."""
    location_lower = location.lower()
    
    for category, keywords in config.LOCATION_CATEGORIES.items():
        if any(keyword in location_lower for keyword in keywords):
            return category.title()
    
    return "Other"

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate approximate distance between two coordinates in kilometers."""
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1
    distance = np.sqrt(lat_diff**2 + lon_diff**2) * 111
    return round(distance, 2)

def format_time(hour: int) -> str:
    """Format hour as readable time string."""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour-12}:00 PM"

def get_time_category(hour: int) -> str:
    """Get time category for a given hour."""
    for category, (start, end) in config.TIME_CATEGORIES.items():
        if start <= hour < end:
            return category.replace('_', ' ').title()
    return "Unknown"

def get_group_size_category(passengers: int) -> str:
    """Get group size category for passenger count."""
    for category, (min_size, max_size) in config.GROUP_SIZE_CATEGORIES.items():
        if min_size <= passengers <= max_size:
            return category.replace('_', ' ').title()
    return "Unknown"

def extract_numbers_from_text(text: str) -> List[int]:
    """Extract all numbers from text."""
    numbers = re.findall(r'\d+', text)
    return [int(num) for num in numbers]

def parse_date_string(date_str: str) -> Optional[datetime]:
    """Parse various date string formats."""
    formats = [
        '%m/%d/%y %H:%M',
        '%m/%d/%Y %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%m/%d/%y %H:%M:%S'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def generate_insights(data: pd.DataFrame) -> Dict[str, Any]:
    """Generate comprehensive insights from trip data."""
    insights = {}
    
    insights['total_trips'] = len(data)
    insights['total_passengers'] = data['Total Passengers'].sum()
    insights['avg_group_size'] = data['Total Passengers'].mean()
    insights['median_group_size'] = data['Total Passengers'].median()
    
    if 'hour' in data.columns:
        insights['peak_hour'] = data['hour'].mode().iloc[0] if len(data['hour'].mode()) > 0 else None
        insights['hour_distribution'] = data['hour'].value_counts().to_dict()
    
    if 'pickup_main' in data.columns:
        insights['top_pickups'] = data['pickup_main'].value_counts().head(10).to_dict()
        insights['unique_pickup_locations'] = data['pickup_main'].nunique()
    
    if 'dropoff_main' in data.columns:
        insights['top_dropoffs'] = data['dropoff_main'].value_counts().head(10).to_dict()
        insights['unique_dropoff_locations'] = data['dropoff_main'].nunique()
    
    insights['group_size_distribution'] = data['Total Passengers'].value_counts().to_dict()
    insights['large_groups'] = len(data[data['Total Passengers'] >= config.ANALYSIS_THRESHOLDS['large_group_threshold']])
    insights['large_groups_percentage'] = (insights['large_groups'] / insights['total_trips']) * 100
    
    if 'date' in data.columns:
        insights['date_range'] = {
            'start': data['date'].min(),
            'end': data['date'].max(),
            'days_covered': (data['date'].max() - data['date'].min()).days + 1
        }
        insights['daily_average'] = insights['total_trips'] / insights['date_range']['days_covered']
    
    return insights

def format_number(number: float, decimals: int = 1) -> str:
    """Format numbers for display."""
    if number >= 1000000:
        return f"{number/1000000:.{decimals}f}M"
    elif number >= 1000:
        return f"{number/1000:.{decimals}f}K"
    else:
        return f"{number:.{decimals}f}" if decimals > 0 else str(int(number))

def create_summary_stats(data: pd.DataFrame) -> Dict[str, str]:
    """Create formatted summary statistics for display."""
    insights = generate_insights(data)
    
    return {
        'Total Trips': format_number(insights['total_trips'], 0),
        'Total Passengers': format_number(insights['total_passengers'], 0),
        'Average Group Size': f"{insights['avg_group_size']:.1f}",
        'Peak Hour': format_time(insights.get('peak_hour', 22)),
        'Large Groups': f"{insights['large_groups_percentage']:.1f}%",
        'Unique Pickup Locations': format_number(insights.get('unique_pickup_locations', 0), 0),
        'Unique Destinations': format_number(insights.get('unique_dropoff_locations', 0), 0),
        'Daily Average': f"{insights.get('daily_average', 0):.1f} trips/day"
    }

def validate_data(data: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate data quality and return issues found."""
    issues = []
    
    required_columns = ['Trip ID', 'Total Passengers', 'Trip Date and Time']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        issues.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    if len(data) == 0:
        issues.append("Dataset is empty")
        return False, issues
    
    if 'Total Passengers' in data.columns:
        invalid_passengers = data[
            (data['Total Passengers'] < 1) | 
            (data['Total Passengers'] > 20) | 
            (data['Total Passengers'].isna())
        ]
        if len(invalid_passengers) > 0:
            issues.append(f"Found {len(invalid_passengers)} trips with invalid passenger counts")
    
    if 'Trip Date and Time' in data.columns:
        invalid_dates = 0
        for date_str in data['Trip Date and Time'].dropna():
            if parse_date_string(str(date_str)) is None:
                invalid_dates += 1
        if invalid_dates > 0:
            issues.append(f"Found {invalid_dates} trips with invalid date formats")
    
    if 'Trip ID' in data.columns:
        duplicates = data['Trip ID'].duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate trip IDs")
    
    return len(issues) == 0, issues

def create_export_data(data: pd.DataFrame, insights: Dict[str, Any], format_type: str = 'csv') -> Any:
    """Create data for export in specified format."""
    if format_type == 'csv':
        return data.to_csv(index=False)
    
    elif format_type == 'json':
        export_data = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'total_records': len(data),
                'insights': insights
            },
            'data': data.to_dict('records')
        }
        return export_data
    
    elif format_type == 'summary':
        summary = create_summary_stats(data)
        return summary
    
    else:
        raise ValueError(f"Unsupported export format: {format_type}")

def search_locations(query: str, locations: List[str], max_results: int = 5) -> List[str]:
    """Search for locations matching a query."""
    query_lower = query.lower()
    matches = []
    
    for location in locations:
        if query_lower == location.lower():
            matches.append(location)
    
    for location in locations:
        if query_lower in location.lower() and location not in matches:
            matches.append(location)
    
    query_words = query_lower.split()
    for location in locations:
        location_lower = location.lower()
        if (any(word in location_lower for word in query_words) and 
            location not in matches):
            matches.append(location)
    
    return matches[:max_results]

def get_color_palette(num_colors: int) -> List[str]:
    """Get a color palette for visualizations."""
    base_colors = [
        '#667eea', '#764ba2', '#f093fb', '#f5576c',
        '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
        '#ffecd2', '#fcb69f', '#a8edea', '#fed6e3'
    ]
    
    if num_colors <= len(base_colors):
        return base_colors[:num_colors]
    
    import colorsys
    additional_colors = []
    for i in range(num_colors - len(base_colors)):
        hue = (i * 0.618033988749895) % 1
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        hex_color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb)
        additional_colors.append(hex_color)
    
    return base_colors + additional_colors