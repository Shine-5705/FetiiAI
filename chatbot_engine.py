import re
from typing import Dict, List, Any, Tuple
from data_processor import DataProcessor
import utils

class FetiiChatbot:
    """
    GPT-style chatbot that can answer questions about Fetii rideshare data.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """Initialize the chatbot with a data processor."""
        self.data_processor = data_processor
        self.conversation_history = []
        
        self.query_patterns = {
            'location_stats': [
                r'how many.*(?:groups?|trips?).*(?:went to|to|from)\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'(?:trips?|groups?).*(?:to|from)\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'tell me about\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'stats for\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'(?:show me|find|search)\s+([^?]+?)(?:\s+(?:trips?|data|stats))?(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$'
            ],
            'time_patterns': [
                r'when do.*groups?.*ride',
                r'what time.*most popular',
                r'peak hours?',
                r'busiest time'
            ],
            'group_size': [
                r'large groups?\s*\((\d+)\+?\)',
                r'groups? of (\d+)\+? riders?',
                r'(\d+)\+? passengers?',
                r'group size'
            ],
            'top_locations': [
                r'top.*(?:pickup|drop-?off).*spots?',
                r'most popular.*locations?',
                r'busiest.*locations?',
                r'hottest spots?',
                r'show.*(?:pickup|drop-?off|locations?)',
                r'list.*locations?'
            ],
            'demographics': [
                r'(\d+)[-–](\d+) year[- ]olds?',
                r'age group',
                r'demographics?'
            ],
            'general_stats': [
                r'how many total',
                r'average group size',
                r'summary',
                r'overview',
                r'give me.*overview',
                r'show me.*stats',
                r'total trips'
            ]
        }
        
        self.time_patterns = [
            r'\s+(?:last|this|yesterday|today)\s+(?:week|month|year|night)',
            r'\s+(?:last|this)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'\s+(?:in\s+)?(?:january|february|march|april|may|june|july|august|september|october|november|december)',
            r'\s+(?:last|this|next)\s+\w+',
            r'\s+(?:yesterday|today|tonight)',
            r'\s+\d{1,2}\/\d{1,2}\/\d{2,4}',
            r'\s+\d{1,2}-\d{1,2}-\d{2,4}'
        ]
    
    def process_query(self, user_query: str) -> str:
        """Process a user query and return an appropriate response."""
        user_query = user_query.lower().strip()
        
        self.conversation_history.append({"role": "user", "content": user_query})
        
        try:
            query_type, params = self._parse_query(user_query)
            response = self._generate_response(query_type, params, user_query)
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_response = ("I'm having trouble understanding that question. "
                            "Try asking about specific locations, times, or group sizes. "
                            "For example: 'How many groups went to The Aquarium on 6th?' or "
                            "'What are the peak hours for large groups?'")
            return error_response
    
    def _clean_location_from_query(self, location_text: str) -> str:
        """Clean time references from location text."""
        cleaned = location_text.strip()
        
        for pattern in self.time_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _parse_query(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """Parse the user query to determine intent and extract parameters."""
        params = {}
        
        for pattern in self.query_patterns['location_stats']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                location = self._clean_location_from_query(location)
                if location:
                    params['location'] = location
                    return 'location_stats', params
        
        for pattern in self.query_patterns['time_patterns']:
            if re.search(pattern, query, re.IGNORECASE):
                group_match = re.search(r'(\d+)\+?', query)
                if group_match:
                    params['min_group_size'] = int(group_match.group(1))
                return 'time_patterns', params
        
        for pattern in self.query_patterns['group_size']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if match.groups():
                    params['group_size'] = int(match.group(1))
                return 'group_size', params
        
        for pattern in self.query_patterns['top_locations']:
            if re.search(pattern, query, re.IGNORECASE):
                if 'pickup' in query or 'pick up' in query:
                    params['location_type'] = 'pickup'
                elif 'drop' in query:
                    params['location_type'] = 'dropoff'
                else:
                    params['location_type'] = 'both'
                return 'top_locations', params
        
        for pattern in self.query_patterns['demographics']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match and match.groups():
                if len(match.groups()) == 2:
                    params['age_range'] = (int(match.group(1)), int(match.group(2)))
                return 'demographics', params
        
        for pattern in self.query_patterns['general_stats']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'general_stats', params
        
        return 'general_stats', params
    
    def _fuzzy_search_location(self, query_location: str) -> List[Tuple[str, int]]:
        """Search for locations using fuzzy matching."""
        all_pickups = self.data_processor.df['pickup_main'].value_counts()
        all_dropoffs = self.data_processor.df['dropoff_main'].value_counts()
        
        all_locations = {}
        for location, count in all_pickups.items():
            all_locations[location] = all_locations.get(location, 0) + count
        for location, count in all_dropoffs.items():
            all_locations[location] = all_locations.get(location, 0) + count
        
        matches = []
        query_lower = query_location.lower()
        
        # Exact match
        for location, count in all_locations.items():
            if query_lower == location.lower():
                matches.append((location, count))
        
        # Partial match
        if not matches:
            for location, count in all_locations.items():
                if query_lower in location.lower() or location.lower() in query_lower:
                    matches.append((location, count))
        
        # Word match
        if not matches:
            query_words = query_lower.split()
            for location, count in all_locations.items():
                location_lower = location.lower()
                if any(word in location_lower for word in query_words if len(word) > 2):
                    matches.append((location, count))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:5] 
    
    def _generate_response(self, query_type: str, params: Dict[str, Any], original_query: str) -> str:
        """Generate a response based on the query type and parameters."""
        
        if query_type == 'location_stats':
            return self._handle_location_stats(params, original_query)
        elif query_type == 'time_patterns':
            return self._handle_time_patterns(params)
        elif query_type == 'group_size':
            return self._handle_group_size(params)
        elif query_type == 'top_locations':
            return self._handle_top_locations(params)
        elif query_type == 'demographics':
            return self._handle_demographics(params)
        elif query_type == 'general_stats':
            return self._handle_general_stats()
        else:
            return self._handle_fallback(original_query)
    
    def _handle_location_stats(self, params: Dict[str, Any], original_query: str) -> str:
        """Handle location-specific statistics queries."""
        location = params.get('location', '')
        
        stats = self.data_processor.get_location_stats(location)
        
        if stats['pickup_count'] == 0 and stats['dropoff_count'] == 0:
            matches = self._fuzzy_search_location(location)
            
            if matches:
                best_match = matches[0][0]
                stats = self.data_processor.get_location_stats(best_match)
                
                if stats['pickup_count'] > 0 or stats['dropoff_count'] > 0:
                    response = f"<strong>Found results for '{best_match}'</strong> (closest match to '{location}'):\n\n"
                else:
                    response = f"I couldn't find exact data for '{location}'. Did you mean one of these?\n\n"
                    for match_location, count in matches[:3]:
                        response += f"• <strong>{match_location}</strong> ({count} total trips)\n"
                    response += f"\nTry asking: 'Tell me about {matches[0][0]}'"
                    return response
            else:
                return f"I couldn't find any trips associated with '{location}'. Try checking the spelling or asking about a different location like 'West Campus' or 'The Aquarium on 6th'."
        else:
            best_match = location.title()
            response = f"<strong>Stats for {best_match}:</strong>\n\n"
        
        if stats['pickup_count'] > 0:
            response += f"<strong>{stats['pickup_count']} pickup trips</strong> with an average group size of {stats['avg_group_size_pickup']:.1f}\n"
            if stats['peak_hours_pickup']:
                peak_hours = ', '.join([utils.format_time(h) for h in stats['peak_hours_pickup']])
                response += f"Most popular pickup times: {peak_hours}\n"
        
        if stats['dropoff_count'] > 0:
            response += f"<strong>{stats['dropoff_count']} drop-off trips</strong> with an average group size of {stats['avg_group_size_dropoff']:.1f}\n"
            if stats['peak_hours_dropoff']:
                peak_hours = ', '.join([utils.format_time(h) for h in stats['peak_hours_dropoff']])
                response += f"Most popular drop-off times: {peak_hours}\n"
        
        total_trips = stats['pickup_count'] + stats['dropoff_count']
        insights = self.data_processor.get_quick_insights()
        percentage = (total_trips / insights['total_trips']) * 100
        
        response += f"\n<strong>Insight:</strong> This location accounts for {percentage:.1f}% of all Austin trips!"
        
        if any(word in original_query for word in ['last', 'this', 'month', 'week', 'yesterday', 'today']):
            response += f"\n\n<strong>Note:</strong> This data covers our full Austin dataset. For specific time periods, the patterns shown represent typical activity for this location."
        
        return response
    
    def _handle_time_patterns(self, params: Dict[str, Any]) -> str:
        """Handle time pattern queries."""
        min_group_size = params.get('min_group_size', None)
        
        time_data = self.data_processor.get_time_patterns(min_group_size)
        
        response = "<strong>Peak Riding Times:</strong>\n\n"
        
        if min_group_size:
            response += f"<em>For groups of {min_group_size}+ riders:</em>\n\n"
        
        hourly_counts = time_data['hourly_counts']
        top_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response += "<strong>Busiest Hours:</strong>\n"
        for i, (hour, count) in enumerate(top_hours, 1):
            time_label = utils.format_time(hour)
            response += f"{i}. <strong>{time_label}</strong> - {count} trips\n"
        
        time_categories = time_data['time_category_counts']
        response += "\n<strong>By Time Period:</strong>\n"
        for period, count in sorted(time_categories.items(), key=lambda x: x[1], reverse=True):
            response += f"• <strong>{period}:</strong> {count} trips\n"
        
        peak_hour = top_hours[0][0]
        peak_count = top_hours[0][1]
        response += f"\n<strong>Insight:</strong> {utils.format_time(peak_hour)} is the absolute peak with {peak_count} trips!"
        
        return response
    
    def _handle_group_size(self, params: Dict[str, Any]) -> str:
        """Handle group size queries."""
        target_size = params.get('group_size', 6)
        
        insights = self.data_processor.get_quick_insights()
        group_distribution = insights['group_size_distribution']
        
        response = f"<strong>Group Size Analysis ({target_size}+ passengers):</strong>\n\n"
        
        large_group_trips = sum(count for size, count in group_distribution.items() if size >= target_size)
        total_trips = insights['total_trips']
        percentage = (large_group_trips / total_trips) * 100
        
        response += f"• <strong>{large_group_trips} trips</strong> had {target_size}+ passengers ({percentage:.1f}% of all trips)\n"
        
        response += f"\n<strong>Breakdown of {target_size}+ passenger groups:</strong>\n"
        large_groups = {size: count for size, count in group_distribution.items() if size >= target_size}
        for size, count in sorted(large_groups.items(), key=lambda x: x[1], reverse=True)[:8]:
            group_pct = (count / large_group_trips) * 100 if large_group_trips > 0 else 0
            response += f"• <strong>{size} passengers:</strong> {count} trips ({group_pct:.1f}%)\n"
        
        avg_size = insights['avg_group_size']
        response += f"\n<strong>Insight:</strong> Average group size is {avg_size:.1f} passengers - most rides are group experiences!"
        
        return response
    
    def _handle_top_locations(self, params: Dict[str, Any]) -> str:
        """Handle top locations queries."""
        location_type = params.get('location_type', 'both')
        insights = self.data_processor.get_quick_insights()
        
        response = "<strong>Most Popular Locations:</strong>\n\n"
        
        if location_type in ['pickup', 'both']:
            response += "<strong>Top Pickup Spots:</strong>\n"
            for i, (location, count) in enumerate(list(insights['top_pickups'])[:8], 1):
                response += f"{i}. <strong>{location}</strong> - {count} pickups\n"
        
        if location_type in ['dropoff', 'both']:
            if location_type == 'both':
                response += "\n<strong>Top Drop-off Destinations:</strong>\n"
            else:
                response += "<strong>Top Drop-off Destinations:</strong>\n"
            for i, (location, count) in enumerate(list(insights['top_dropoffs'])[:8], 1):
                response += f"{i}. <strong>{location}</strong> - {count} drop-offs\n"
        
        if location_type in ['pickup', 'both']:
            top_pickup = list(insights['top_pickups'])[0]
            response += f"\n<strong>Insight:</strong> {top_pickup[0]} dominates pickups with {top_pickup[1]} trips!"
        
        return response
    
    def _handle_demographics(self, params: Dict[str, Any]) -> str:
        """Handle demographics queries."""
        age_range = params.get('age_range', (18, 24))
        
        response = f"<strong>Demographics Analysis ({age_range[0]}-{age_range[1]} year olds):</strong>\n\n"
        response += "I'd love to help with demographic analysis, but I don't currently have access to rider age data in this dataset. "
        response += "However, I can tell you about the locations and times that are popular with different group sizes!\n\n"
        
        insights = self.data_processor.get_quick_insights()
        response += "<strong>Popular spots that might appeal to younger riders:</strong>\n"
        
        entertainment_spots = ['The Aquarium on 6th', 'Wiggle Room', "Shakespeare's", 'LUNA Rooftop', 'Green Light Social']
        
        for spot in entertainment_spots[:5]:
            for location, count in insights['top_dropoffs']:
                if spot.lower() in location.lower():
                    response += f"• <strong>{location}</strong> - {count} drop-offs\n"
                    break
        
        response += "\n<strong>Insight:</strong> Late night hours (10 PM - 1 AM) see the highest activity, which often correlates with younger demographics!"
        
        return response
    
    def _handle_general_stats(self) -> str:
        """Handle general statistics queries."""
        insights = self.data_processor.get_quick_insights()
        
        response = "<strong>Fetii Austin Overview:</strong>\n\n"
        
        response += f"<strong>Total Trips Analyzed:</strong> {insights['total_trips']:,}\n"
        response += f"<strong>Average Group Size:</strong> {insights['avg_group_size']:.1f} passengers\n"
        response += f"<strong>Peak Hour:</strong> {utils.format_time(insights['peak_hour'])}\n"
        response += f"<strong>Large Groups (6+):</strong> {insights['large_groups_count']} trips ({insights['large_groups_pct']:.1f}%)\n\n"
        
        response += "<strong>Top Hotspots:</strong>\n"
        top_pickup = list(insights['top_pickups'])[0]
        top_dropoff = list(insights['top_dropoffs'])[0]
        response += f"• Most popular pickup: <strong>{top_pickup[0]}</strong> ({top_pickup[1]} trips)\n"
        response += f"• Most popular destination: <strong>{top_dropoff[0]}</strong> ({top_dropoff[1]} trips)\n\n"
        
        group_dist = insights['group_size_distribution']
        most_common_size = max(group_dist.items(), key=lambda x: x[1])
        response += f"<strong>Most Common Group Size:</strong> {most_common_size[0]} passengers ({most_common_size[1]} trips)\n\n"
        
        response += "<strong>Key Insights:</strong>\n"
        response += f"• {insights['large_groups_pct']:.0f}% of all rides are large groups (6+ people)\n"
        response += "• Peak activity happens late evening (10-11 PM)\n"
        response += "• West Campus dominates as the top pickup location\n"
        response += "• Entertainment venues are the most popular destinations"
        
        return response
    
    def _handle_fallback(self, query: str) -> str:
        """Handle queries that don't match any specific pattern."""
        response = "I'm not sure I understood that question perfectly. Here's what I can help you with:\n\n"
        
        response += "<strong>Location Questions:</strong>\n"
        response += "• 'How many groups went to [location]?'\n"
        response += "• 'Tell me about [location]'\n"
        response += "• 'Top pickup/drop-off spots'\n\n"
        
        response += "<strong>Time Questions:</strong>\n"
        response += "• 'When do large groups typically ride?'\n"
        response += "• 'Peak hours for groups of 6+'\n"
        response += "• 'Busiest times'\n\n"
        
        response += "<strong>Group Size Questions:</strong>\n"
        response += "• 'How many trips had 10+ passengers?'\n"
        response += "• 'Large group patterns'\n"
        response += "• 'Average group size'\n\n"
        
        response += "Would you like to try asking one of these types of questions?"
        
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []