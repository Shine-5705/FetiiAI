"""
Configuration settings for Fetii AI Chatbot
"""

CSV_FILE_PATH = "fetii_data.csv"
SAMPLE_DATA_SIZE = 2000

APP_TITLE = "Fetii AI Assistant"
APP_ICON = "🚗"
PAGE_LAYOUT = "wide"

COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#4caf50',
    'info': '#2196f3',
    'warning': '#ff9800',
    'danger': '#f44336',
    'light': '#f8f9fa',
    'dark': '#2c3e50'
}

CHART_CONFIG = {
    'height': 300,
    'margin': dict(t=50, b=50, l=50, r=50),
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font_color': '#2c3e50'
}

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

LOCATION_CATEGORIES = {
    'entertainment': ['bar', 'club', 'lounge', 'aquarium', 'rooftop', 'social', 'pub', 'restaurant'],
    'campus': ['campus', 'university', 'drag', 'west campus', 'student'],
    'residential': ['house', 'apartment', 'residence', 'home'],
    'business': ['office', 'building', 'center', 'district'],
    'transport': ['airport', 'station', 'terminal', 'stop']
}

TIME_CATEGORIES = {
    'morning': (6, 12),
    'afternoon': (12, 17),
    'evening': (17, 21),
    'night': (21, 24),
    'late_night': (0, 6)
}

GROUP_SIZE_CATEGORIES = {
    'small': (1, 4),
    'medium': (5, 8),
    'large': (9, 12),
    'extra_large': (13, 20)
}

ANALYSIS_THRESHOLDS = {
    'min_trips_for_pattern': 5,
    'peak_hour_threshold': 0.8,
    'popular_location_threshold': 10,
    'large_group_threshold': 6
}

EXPORT_CONFIG = {
    'formats': ['csv', 'json', 'pdf'],
    'max_export_rows': 10000,
    'include_visualizations': True
}