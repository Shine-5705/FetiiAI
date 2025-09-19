import re
import json
import requests
from typing import Dict, List, Any, Tuple, Optional
from data_processor import DataProcessor
import utils

class EnhancedFetiiChatbot:
    """
    Enhanced conversational chatbot with Google Gemini AI integration for Fetii rideshare data analysis.
    Falls back to pattern-based responses when AI is unavailable.
    """
    
    def __init__(self, data_processor: DataProcessor, use_ai: bool = True, gemini_api_key: str = None):
        """Initialize the enhanced chatbot with Gemini AI capabilities."""
        self.data_processor = data_processor
        self.conversation_history = []
        self.use_ai = use_ai
        self.gemini_api_key = gemini_api_key
        self.ai_available = False
        
        # Initialize Gemini AI if API key provided
        if self.use_ai and self.gemini_api_key:
            self._setup_gemini()
        
        # Fallback pattern-based system
        self.query_patterns = {
            'greetings': [
                r'^(?:hi|hello|hey|good morning|good afternoon|good evening|greetings?)(?:\s+.*)?$',
                r'^(?:what\'?s up|how are you|how\'?s it going|sup)(?:\s+.*)?$',
                r'^(?:thanks?|thank you|thx|appreciate it)(?:\s+.*)?$'
            ],
            'casual_conversation': [
                r'^(?:how are you|what are you|who are you|what can you do)(?:\s+.*)?$',
                r'^(?:tell me about yourself|what\'?s your name|introduce yourself)(?:\s+.*)?$',
                r'^(?:help|what can you help with|what do you do)(?:\s+.*)?$',
                r'^(?:i\'?m (?:good|fine|okay|great|tired|busy))(?:\s+.*)?$'
            ],
            'location_stats': [
                r'how many.*(?:groups?|trips?).*(?:went to|to|from)\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'(?:trips?|groups?).*(?:to|from)\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'tell me about\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
                r'stats for\s+([^?]+?)(?:\s+(?:last|this|yesterday|today|week|month|year).*?)?[?.]?$',
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
    
    def _setup_gemini(self):
        """Setup Gemini AI connection."""
        try:
            # Test Gemini API connection with minimal request
            test_payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "Hi"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 10
                }
            }
            
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.gemini_api_key}',
                headers={'Content-Type': 'application/json'},
                json=test_payload,
                timeout=5
            )
            
            if response.status_code == 200:
                self.ai_available = True
                print("✅ Gemini AI connected successfully")
            elif response.status_code == 429:
                print("⚠️ Gemini API rate limit reached - falling back to pattern-based responses")
                self.ai_available = False
            elif response.status_code == 400:
                print("⚠️ Invalid Gemini API key or request")
                self.ai_available = False
            else:
                print(f"⚠️ Gemini AI connection failed: {response.status_code}")
                self.ai_available = False
                
        except Exception as e:
            print(f"⚠️ Failed to connect to Gemini AI: {str(e)}")
            self.ai_available = False
    
    def process_query(self, user_query: str) -> str:
        """Process a user query and return an appropriate response."""
        user_query = user_query.strip()
        
        self.conversation_history.append({"role": "user", "content": user_query})
        
        try:
            # Get relevant data context
            context = self._get_data_context(user_query)
            
            # Try AI response first if available
            if self.ai_available:
                ai_response = self._get_gemini_response(user_query, context)
                if ai_response:
                    self.conversation_history.append({"role": "assistant", "content": ai_response})
                    return ai_response
            
            # Fallback to pattern-based response
            response = self._pattern_based_response(user_query.lower())
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
            
        except Exception as e:
            error_response = ("I'm having a bit of trouble processing that request. "
                            "Let me help you explore Austin rideshare data - try asking about specific locations, "
                            "time patterns, or group sizes. What would you like to discover?")
            return error_response
    
    def _get_data_context(self, query: str) -> str:
        """Extract relevant data context based on the query."""
        insights = self.data_processor.get_quick_insights()
        query_lower = query.lower()
        
        # Base context always included
        context_parts = [
            f"Total Austin rideshare trips analyzed: {insights['total_trips']:,}",
            f"Average group size: {insights['avg_group_size']:.1f} passengers",
            f"Peak activity hour: {utils.format_time(insights['peak_hour'])}",
            f"Large groups (6+): {insights['large_groups_pct']:.1f}% of all trips"
        ]
        
        # Add query-specific context
        if any(word in query_lower for word in ['location', 'place', 'pickup', 'dropoff', 'where', 'destination']):
            top_pickups = dict(list(insights['top_pickups'])[:5])
            top_dropoffs = dict(list(insights['top_dropoffs'])[:5])
            context_parts.extend([
                f"Top pickup locations: {top_pickups}",
                f"Top destinations: {top_dropoffs}"
            ])
        
        if any(word in query_lower for word in ['time', 'hour', 'peak', 'busy', 'when']):
            time_data = self.data_processor.get_time_patterns()
            hourly_top = dict(sorted(time_data['hourly_counts'].items(), key=lambda x: x[1], reverse=True)[:5])
            context_parts.append(f"Hourly trip distribution: {hourly_top}")
        
        if any(word in query_lower for word in ['group', 'size', 'passenger', 'people']):
            group_dist = dict(list(insights['group_size_distribution'].items())[:8])
            context_parts.append(f"Group size distribution: {group_dist}")
        
        # Extract specific location if mentioned
        potential_locations = self._extract_locations_from_query(query)
        if potential_locations:
            for location in potential_locations[:2]:  # Limit to 2 locations
                stats = self.data_processor.get_location_stats(location)
                if stats['pickup_count'] > 0 or stats['dropoff_count'] > 0:
                    context_parts.append(
                        f"'{location}' stats: {stats['pickup_count']} pickups, "
                        f"{stats['dropoff_count']} dropoffs"
                    )
        
        return "\n".join(context_parts)
    
    def _extract_locations_from_query(self, query: str) -> List[str]:
        """Extract potential location names from the query."""
        # Get all known locations
        all_pickups = self.data_processor.df['pickup_main'].unique()
        all_dropoffs = self.data_processor.df['dropoff_main'].unique()
        all_locations = set(list(all_pickups) + list(all_dropoffs))
        
        query_lower = query.lower()
        found_locations = []
        
        for location in all_locations:
            if location.lower() in query_lower:
                found_locations.append(location)
        
        return found_locations
    
    def _get_gemini_response(self, query: str, context: str) -> Optional[str]:
        """Get response from Gemini AI with improved error handling."""
        try:
            # Create system prompt with data context
            system_prompt = f"""You are Fetii AI, a friendly and knowledgeable assistant specializing in Austin rideshare analytics. 

Your personality:
- Conversational and helpful
- Provide specific data-driven insights
- Use the actual data provided in context
- Format responses clearly with key numbers highlighted
- Be enthusiastic about patterns and trends
- Keep responses concise but informative (under 150 words)

Current Austin rideshare data context:
{context}

Important: Always use the specific numbers and data from the context above. Don't make up statistics.

User query: {query}

Response:"""
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": system_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.gemini_api_key}',
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
            elif response.status_code == 429:
                print("⚠️ Gemini API rate limit reached - falling back to pattern-based response")
                self.ai_available = False
                return None
            elif response.status_code == 400:
                print("⚠️ Invalid Gemini API request")
                self.ai_available = False
                return None
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print("⚠️ Gemini API timeout - falling back to pattern-based response")
            return None
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            
        return None
    
    def _pattern_based_response(self, query: str) -> str:
        """Fallback pattern-based response system."""
        query_type, params = self._parse_query(query)
        
        if query_type == 'greetings':
            return self._handle_greetings(query)
        elif query_type == 'casual_conversation':
            return self._handle_casual_conversation(query)
        elif query_type == 'location_stats':
            return self._handle_location_stats(params, query)
        elif query_type == 'time_patterns':
            return self._handle_time_patterns(params)
        elif query_type == 'group_size':
            return self._handle_group_size(params)
        elif query_type == 'top_locations':
            return self._handle_top_locations(params)
        elif query_type == 'general_stats':
            return self._handle_general_stats()
        else:
            return self._handle_fallback(query)
    
    def _parse_query(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """Parse the user query to determine intent and extract parameters."""
        params = {}
        
        # Check for greetings first
        for pattern in self.query_patterns['greetings']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'greetings', params
        
        # Check for casual conversation
        for pattern in self.query_patterns['casual_conversation']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'casual_conversation', params
        
        # Check for location stats
        for pattern in self.query_patterns['location_stats']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if location:
                    params['location'] = location
                    return 'location_stats', params
        
        # Check other patterns
        for pattern in self.query_patterns['time_patterns']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'time_patterns', params
        
        for pattern in self.query_patterns['group_size']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'group_size', params
        
        for pattern in self.query_patterns['top_locations']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'top_locations', params
        
        for pattern in self.query_patterns['general_stats']:
            if re.search(pattern, query, re.IGNORECASE):
                return 'general_stats', params
        
        return 'general_stats', params
    
    def _handle_greetings(self, query: str) -> str:
        """Handle greeting messages."""
        if any(word in query.lower() for word in ['thanks', 'thank you']):
            return "You're welcome! Happy to help you explore Austin rideshare patterns."
        
        return ("Hello! I'm Fetii AI, your Austin rideshare analytics assistant. "
               "I can help you understand trip patterns, popular locations, peak hours, and group behaviors. "
               "What would you like to explore?")
    
    def _handle_casual_conversation(self, query: str) -> str:
        """Handle casual conversation."""
        query_lower = query.lower()
        
        if any(phrase in query_lower for phrase in ['how are you', 'how\'s it going']):
            return ("I'm doing great, thanks for asking! I'm excited to help you explore Austin rideshare data. "
                   "What aspect of the data interests you most?")
        
        if any(phrase in query_lower for phrase in ['who are you', 'what are you']):
            return ("I'm Fetii AI, your specialized assistant for Austin rideshare analytics! "
                   "I analyze real Austin rideshare data to provide insights about trip patterns, "
                   "popular destinations, peak hours, and group behaviors. What would you like to explore?")
        
        return ("I'm here to help you explore Austin rideshare data! "
               "Ask me about trip patterns, locations, or any trends you're curious about.")
    
    def _handle_location_stats(self, params: Dict[str, Any], query: str) -> str:
        """Handle location-specific queries."""
        location = params.get('location', '')
        stats = self.data_processor.get_location_stats(location)
        
        if stats['pickup_count'] == 0 and stats['dropoff_count'] == 0:
            return f"I couldn't find trips for '{location}'. Try a different location like 'West Campus' or 'Downtown'."
        
        response = f"**Stats for {location.title()}:**\n\n"
        
        if stats['pickup_count'] > 0:
            response += f"**{stats['pickup_count']} pickup trips** with average group size {stats['avg_group_size_pickup']:.1f}\n"
        
        if stats['dropoff_count'] > 0:
            response += f"**{stats['dropoff_count']} drop-off trips** with average group size {stats['avg_group_size_dropoff']:.1f}\n"
        
        return response
    
    def _handle_time_patterns(self, params: Dict[str, Any]) -> str:
        """Handle time pattern queries."""
        time_data = self.data_processor.get_time_patterns()
        hourly_counts = time_data['hourly_counts']
        top_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        response = "**Peak Hours Analysis:**\n\n"
        for i, (hour, count) in enumerate(top_hours, 1):
            response += f"{i}. **{utils.format_time(hour)}** - {count} trips\n"
        
        return response
    
    def _handle_group_size(self, params: Dict[str, Any]) -> str:
        """Handle group size queries."""
        insights = self.data_processor.get_quick_insights()
        response = f"**Group Size Analysis:**\n\n"
        response += f"Average group size: **{insights['avg_group_size']:.1f} passengers**\n"
        response += f"Large groups (6+): **{insights['large_groups_pct']:.1f}%** of all trips"
        return response
    
    def _handle_top_locations(self, params: Dict[str, Any]) -> str:
        """Handle top locations queries."""
        insights = self.data_processor.get_quick_insights()
        response = "**Top Pickup Locations:**\n\n"
        
        for i, (location, count) in enumerate(list(insights['top_pickups'])[:5], 1):
            response += f"{i}. **{location}** - {count} trips\n"
        
        return response
    
    def _handle_general_stats(self) -> str:
        """Handle general statistics queries."""
        insights = self.data_processor.get_quick_insights()
        
        response = "**Austin Rideshare Overview:**\n\n"
        response += f"**Total Trips:** {insights['total_trips']:,}\n"
        response += f"**Average Group Size:** {insights['avg_group_size']:.1f} passengers\n"
        response += f"**Peak Hour:** {utils.format_time(insights['peak_hour'])}\n"
        response += f"**Large Groups:** {insights['large_groups_pct']:.1f}% (6+ passengers)"
        
        return response
    
    def _handle_fallback(self, query: str) -> str:
        """Handle unrecognized queries."""
        return ("I can help you explore Austin rideshare data! Try asking about:\n\n"
               "• Specific locations: 'Tell me about West Campus'\n"
               "• Time patterns: 'What are the peak hours?'\n"
               "• Group sizes: 'How many large groups ride?'\n"
               "• General stats: 'Give me an overview'\n\n"
               "What interests you most?")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def set_gemini_api_key(self, api_key: str):
        """Update Gemini API key and reinitialize connection."""
        self.gemini_api_key = api_key
        if api_key:
            self._setup_gemini()
        else:
            self.ai_available = False