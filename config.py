"""
Configuration settings for Fetii AI Chatbot
"""

# File settings
CSV_FILE_PATH = "fetii_data.csv"
SAMPLE_DATA_SIZE = 2000

# App settings
APP_TITLE = "Fetii AI Assistant"
APP_ICON = "🚗"
PAGE_LAYOUT = "wide"

# Modern color palette
COLORS = {
    'primary': '#3b82f6',      # Blue-500
    'primary_dark': '#1d4ed8',  # Blue-700
    'secondary': '#10b981',     # Emerald-500
    'success': '#059669',       # Emerald-600
    'warning': '#f59e0b',       # Amber-500
    'danger': '#ef4444',        # Red-500
    'info': '#06b6d4',         # Cyan-500
    'light': '#f8fafc',        # Slate-50
    'dark': '#1e293b',         # Slate-800
    'gray_100': '#f1f5f9',     # Slate-100
    'gray_300': '#cbd5e1',     # Slate-300
    'gray_500': '#64748b',     # Slate-500
    'gray_700': '#334155',     # Slate-700
    'gray_900': '#0f172a'      # Slate-900
}

# Chart configuration
CHART_CONFIG = {
    'height': 320,
    'margin': dict(t=60, b=50, l=50, r=50),
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font_color': '#374151',
    'font_family': 'Inter',
    'grid_color': 'rgba(156, 163, 175, 0.2)',
    'line_color': 'rgba(156, 163, 175, 0.3)'
}

# Chatbot configuration
CHATBOT_CONFIG = {
    'max_history': 50,
    'response_delay': 0.5,
    'example_questions': [
        "How many groups went to The Aquarium on 6th last month?",
        "What are the top drop-off spots for large groups on Saturday nights?",
        "When do groups of 6+ riders typically ride downtown?",
        "Show me the busiest pickup locations",
        "What's the pattern for West Campus pickups?",
        "How many trips had more than 10 passengers?"
    ]
}

# Location categories for analysis
LOCATION_CATEGORIES = {
    'entertainment': [
        'bar', 'club', 'lounge', 'aquarium', 'rooftop', 'social', 
        'pub', 'restaurant', 'venue', 'hall', 'theater'
    ],
    'campus': [
        'campus', 'university', 'drag', 'west campus', 'student',
        'dorm', 'residence hall', 'fraternity', 'sorority'
    ],
    'residential': [
        'house', 'apartment', 'residence', 'home', 'complex',
        'condo', 'townhouse', 'manor'
    ],
    'business': [
        'office', 'building', 'center', 'district', 'plaza',
        'tower', 'corporate', 'business'
    ],
    'transport': [
        'airport', 'station', 'terminal', 'stop', 'hub',
        'depot', 'port'
    ],
    'retail': [
        'mall', 'store', 'shop', 'market', 'center',
        'plaza', 'outlet', 'galleria'
    ]
}

# Time categories for analysis
TIME_CATEGORIES = {
    'early_morning': (0, 6),    # 12 AM - 6 AM
    'morning': (6, 12),         # 6 AM - 12 PM
    'afternoon': (12, 17),      # 12 PM - 5 PM
    'evening': (17, 21),        # 5 PM - 9 PM
    'night': (21, 24)           # 9 PM - 12 AM
}

# Group size categories
GROUP_SIZE_CATEGORIES = {
    'small': (1, 4),           # 1-4 passengers
    'medium': (5, 8),          # 5-8 passengers  
    'large': (9, 12),          # 9-12 passengers
    'extra_large': (13, 20)    # 13+ passengers
}

# Analysis thresholds
ANALYSIS_THRESHOLDS = {
    'min_trips_for_pattern': 5,
    'peak_hour_threshold': 0.8,
    'popular_location_threshold': 10,
    'large_group_threshold': 6,
    'min_group_size_for_analysis': 3
}

# Export configuration
EXPORT_CONFIG = {
    'formats': ['csv', 'json', 'pdf'],
    'max_export_rows': 10000,
    'include_visualizations': True,
    'compression': 'gzip'
}

# UI Icons (using simple unicode icons)
ICONS = {
    'trips': '📊',
    'users': '👥', 
    'time': '⏰',
    'location': '📍',
    'chart': '📈',
    'chat': '💬',
    'insights': '💡',
    'pickup': '🚗',
    'dropoff': '🎯',
    'large_groups': '🎉',
    'analytics': '📊',
    'dashboard': '🏠'
}

# Font configuration
FONTS = {
    'primary': 'Inter',
    'monospace': 'JetBrains Mono',
    'sizes': {
        'xs': '0.75rem',
        'sm': '0.875rem', 
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem'
    },
    'weights': {
        'light': 300,
        'normal': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700
    }
}

# Spacing configuration
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    '2xl': '2.5rem',
    '3xl': '3rem'
}

# Border radius configuration
BORDER_RADIUS = {
    'sm': '4px',
    'md': '8px',
    'lg': '12px',
    'xl': '16px',
    '2xl': '20px',
    'full': '9999px'
}

# Shadow configuration
SHADOWS = {
    'sm': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
    'md': '0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px rgba(0, 0, 0, 0.25)'
}

# Animation configuration
ANIMATIONS = {
    'duration': {
        'fast': '0.15s',
        'normal': '0.3s',
        'slow': '0.5s'
    },
    'easing': {
        'ease_in': 'cubic-bezier(0.4, 0, 1, 1)',
        'ease_out': 'cubic-bezier(0, 0, 0.2, 1)',
        'ease_in_out': 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
}

# Responsive breakpoints
BREAKPOINTS = {
    'sm': '640px',
    'md': '768px', 
    'lg': '1024px',
    'xl': '1280px',
    '2xl': '1536px'
}

# Data validation rules
VALIDATION_RULES = {
    'min_passengers': 1,
    'max_passengers': 20,
    'required_fields': ['Trip ID', 'Total Passengers', 'Trip Date and Time'],
    'date_formats': ['%m/%d/%y %H:%M', '%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M:%S'],
    'coordinate_bounds': {
        'lat_min': 30.0,
        'lat_max': 30.5,
        'lng_min': -98.0,
        'lng_max': -97.5
    }
}

# Performance settings
PERFORMANCE = {
    'max_rows_for_visualization': 10000,
    'cache_timeout': 3600,  # 1 hour
    'pagination_size': 50,
    'max_memory_usage': '1GB'
}

# Error messages
ERROR_MESSAGES = {
    'file_not_found': 'Data file not found. Using sample data for demonstration.',
    'invalid_data': 'Invalid data format detected. Please check your data.',
    'no_results': 'No results found for your query. Try adjusting your filters.',
    'processing_error': 'An error occurred while processing your request.',
    'visualization_error': 'Unable to create visualization with current data.'
}

# Success messages
SUCCESS_MESSAGES = {
    'data_loaded': 'Data loaded successfully',
    'export_complete': 'Export completed successfully',
    'analysis_complete': 'Analysis completed',
    'cache_updated': 'Cache updated successfully'
}