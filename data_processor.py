import pandas as pd
import numpy as np
from typing import Dict, Any

class DataProcessor:
    """
    Handles all data processing and analysis for Fetii rideshare data.
    """
    
    def __init__(self, csv_file_path: str = "fetii_data.csv"):
        """Initialize the data processor with the CSV file."""
        self.csv_file_path = csv_file_path
        self.df = None
        self.insights = {}
        self.load_and_process_data()
    
    def load_and_process_data(self):
        """Load and process the Fetii trip data."""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            
            self._clean_data()
            self._extract_temporal_features()
            self._extract_location_features()
            self._calculate_insights()
            
            print(f"✅ Successfully loaded {len(self.df)} trips from Austin")
            
        except FileNotFoundError:
            print("⚠️ CSV file not found. Creating sample data for demo...")
            self._create_sample_data()
    
    def _create_sample_data(self):
        """Create sample data based on the analysis patterns."""
        np.random.seed(42)
        
        locations = {
            'pickup': ['West Campus', 'The Drag', 'Market District', 'Sixth Street', 'East End', 
                      'Downtown', 'Govalle', 'Hancock', 'South Lamar', 'Warehouse District'],
            'dropoff': ['The Aquarium on 6th', 'Wiggle Room', "Shakespeare's", 'Mayfair Austin', 
                       'Latchkey', '6013 Loyola Ln', "Buford's", 'Darrell K Royal Texas Memorial Stadium',
                       'LUNA Rooftop', 'University of Texas KA house', 'Green Light Social', "The Cat's Pajamas"]
        }
        
        passenger_choices = [14, 8, 7, 10, 9, 12, 11, 13, 6, 5, 4, 3, 2, 1]
        passenger_weights = [0.173, 0.128, 0.120, 0.115, 0.113, 0.087, 0.085, 0.077, 0.063, 0.028, 0.007, 0.004, 0.001, 0.001]
        
        hour_choices = [22, 23, 21, 19, 0, 20, 18, 1, 2, 17, 16, 3]
        hour_weights = [0.25, 0.23, 0.19, 0.11, 0.08, 0.06, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01]
        
        sample_data = []
        for i in range(2000):
            passengers = np.random.choice(passenger_choices, p=passenger_weights)
            hour = np.random.choice(hour_choices, p=hour_weights)
            
            pickup_lat = np.random.normal(30.2672, 0.02)
            pickup_lng = np.random.normal(-97.7431, 0.02)
            dropoff_lat = np.random.normal(30.2672, 0.02)
            dropoff_lng = np.random.normal(-97.7431, 0.02)
            
            day = np.random.randint(1, 31)
            minute = np.random.randint(0, 60)
            
            sample_data.append({
                'Trip ID': 734889 - i,
                'Booking User ID': np.random.randint(10000, 999999),
                'Pick Up Latitude': pickup_lat,
                'Pick Up Longitude': pickup_lng,
                'Drop Off Latitude': dropoff_lat,
                'Drop Off Longitude': dropoff_lng,
                'Pick Up Address': f"{np.random.choice(locations['pickup'])}, Austin, TX",
                'Drop Off Address': f"{np.random.choice(locations['dropoff'])}, Austin, TX",
                'Trip Date and Time': f"9/{day}/25 {hour}:{minute:02d}",
                'Total Passengers': passengers
            })
        
        self.df = pd.DataFrame(sample_data)
        self._clean_data()
        self._extract_temporal_features()
        self._extract_location_features()
        self._calculate_insights()
    
    def _clean_data(self):
        """Clean and standardize the data."""
        self.df = self.df.dropna(subset=['Total Passengers', 'Trip Date and Time'])
        
        self.df['Total Passengers'] = self.df['Total Passengers'].astype(int)
        
        self.df['pickup_main'] = self.df['Pick Up Address'].apply(self._extract_main_location)
        self.df['dropoff_main'] = self.df['Drop Off Address'].apply(self._extract_main_location)
    
    def _extract_main_location(self, address: str) -> str:
        """Extract the main location name from an address."""
        if pd.isna(address):
            return "Unknown"
        return address.split(',')[0].strip()
    
    def _extract_temporal_features(self):
        """Extract temporal features from trip data."""
        self.df['datetime'] = pd.to_datetime(self.df['Trip Date and Time'], format='%m/%d/%y %H:%M')
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.day_name()
        self.df['date'] = self.df['datetime'].dt.date
        
        self.df['time_category'] = self.df['hour'].apply(self._categorize_time)
    
    def _categorize_time(self, hour: int) -> str:
        """Categorize hour into time periods."""
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        elif 21 <= hour <= 23:
            return "Night"
        else:
            return "Late Night"
    
    def _extract_location_features(self):
        """Extract location-based features."""
        self.df['group_category'] = self.df['Total Passengers'].apply(self._categorize_group_size)
        
        self.df['is_entertainment'] = self.df['dropoff_main'].apply(self._is_entertainment_venue)
        self.df['is_campus'] = self.df['pickup_main'].apply(self._is_campus_location)
    
    def _categorize_group_size(self, passengers: int) -> str:
        """Categorize group size."""
        if passengers <= 4:
            return "Small (1-4)"
        elif passengers <= 8:
            return "Medium (5-8)"
        elif passengers <= 12:
            return "Large (9-12)"
        else:
            return "Extra Large (13+)"
    
    def _is_entertainment_venue(self, location: str) -> bool:
        """Check if location is an entertainment venue."""
        entertainment_keywords = ['bar', 'club', 'lounge', 'aquarium', 'rooftop', 'social', 'pub']
        return any(keyword in location.lower() for keyword in entertainment_keywords)
    
    def _is_campus_location(self, location: str) -> bool:
        """Check if location is campus-related."""
        campus_keywords = ['campus', 'university', 'drag', 'west campus']
        return any(keyword in location.lower() for keyword in campus_keywords)
    
    def _calculate_insights(self):
        """Calculate key insights from the data."""
        self.insights = {
            'total_trips': len(self.df),
            'avg_group_size': self.df['Total Passengers'].mean(),
            'peak_hour': self.df['hour'].mode().iloc[0],
            'large_groups_count': len(self.df[self.df['Total Passengers'] >= 6]),
            'large_groups_pct': (len(self.df[self.df['Total Passengers'] >= 6]) / len(self.df)) * 100,
            'top_pickups': list(self.df['pickup_main'].value_counts().head(10).items()),
            'top_dropoffs': list(self.df['dropoff_main'].value_counts().head(10).items()),
            'hourly_distribution': self.df['hour'].value_counts().sort_index().to_dict(),
            'group_size_distribution': self.df['Total Passengers'].value_counts().sort_index().to_dict()
        }
    
    def get_quick_insights(self) -> Dict[str, Any]:
        """Get quick insights for dashboard."""
        return self.insights
    
    def query_data(self, query_params: Dict[str, Any]) -> pd.DataFrame:
        """Query the data based on parameters."""
        filtered_df = self.df.copy()
        
        if 'pickup_location' in query_params:
            filtered_df = filtered_df[filtered_df['pickup_main'].str.contains(
                query_params['pickup_location'], case=False, na=False)]
        
        if 'dropoff_location' in query_params:
            filtered_df = filtered_df[filtered_df['dropoff_main'].str.contains(
                query_params['dropoff_location'], case=False, na=False)]
        
        if 'hour_range' in query_params:
            start_hour, end_hour = query_params['hour_range']
            filtered_df = filtered_df[
                (filtered_df['hour'] >= start_hour) & (filtered_df['hour'] <= end_hour)]
        
        if 'min_passengers' in query_params:
            filtered_df = filtered_df[filtered_df['Total Passengers'] >= query_params['min_passengers']]
        
        if 'max_passengers' in query_params:
            filtered_df = filtered_df[filtered_df['Total Passengers'] <= query_params['max_passengers']]
        
        if 'date_range' in query_params:
            start_date, end_date = query_params['date_range']
            filtered_df = filtered_df[
                (filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]
        
        return filtered_df
    
    def get_location_stats(self, location: str, location_type: str = 'both') -> Dict[str, Any]:
        """Get statistics for a specific location."""
        if location_type in ['pickup', 'both']:
            pickup_data = self.df[self.df['pickup_main'].str.contains(location, case=False, na=False)]
        else:
            pickup_data = pd.DataFrame()
        
        if location_type in ['dropoff', 'both']:
            dropoff_data = self.df[self.df['dropoff_main'].str.contains(location, case=False, na=False)]
        else:
            dropoff_data = pd.DataFrame()
        
        return {
            'pickup_count': len(pickup_data),
            'dropoff_count': len(dropoff_data),
            'avg_group_size_pickup': pickup_data['Total Passengers'].mean() if len(pickup_data) > 0 else 0,
            'avg_group_size_dropoff': dropoff_data['Total Passengers'].mean() if len(dropoff_data) > 0 else 0,
            'peak_hours_pickup': pickup_data['hour'].mode().tolist() if len(pickup_data) > 0 else [],
            'peak_hours_dropoff': dropoff_data['hour'].mode().tolist() if len(dropoff_data) > 0 else []
        }
    
    def get_time_patterns(self, group_size_filter: int = None) -> Dict[str, Any]:
        """Get time-based patterns."""
        data = self.df.copy()
        
        if group_size_filter:
            data = data[data['Total Passengers'] >= group_size_filter]
        
        return {
            'hourly_counts': data['hour'].value_counts().sort_index().to_dict(),
            'daily_counts': data['day_of_week'].value_counts().to_dict(),
            'time_category_counts': data['time_category'].value_counts().to_dict()
        }