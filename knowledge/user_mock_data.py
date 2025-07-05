# knowledge/user_mock_data.py
"""
Mock user history, preferences, and profile data for Travel Assistant Chatbot
"""

user_mock_data = {
    "user_id": "user_001",
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "+44 7911 123456",
    "country": "United Kingdom",
    "birthdate": "1990-04-12",
    "gender": "female",
    "passport": {
        "number": "123456789",
        "country": "UK",
        "expiry": "2030-05-01"
    },
    "travel_history": [
        {"destination": "Paris", "date": "2023-05-10", "purpose": "vacation", "duration": 7, "companions": ["partner"], "accommodation": "hotel", "rating": 4.5},
        {"destination": "Tokyo", "date": "2022-11-15", "purpose": "business", "duration": 5, "companions": [], "accommodation": "business hotel", "rating": 4.0},
        {"destination": "Rome", "date": "2021-09-20", "purpose": "honeymoon", "duration": 10, "companions": ["partner"], "accommodation": "boutique hotel", "rating": 5.0},
        {"destination": "Barcelona", "date": "2020-07-18", "purpose": "family", "duration": 8, "companions": ["family"], "accommodation": "apartment", "rating": 4.2}
    ],
    "preferences": {
        "budget": "mid-range",
        "accommodation": ["hotel", "boutique hotel", "apartment"],
        "transport": ["flight", "train"],
        "food": ["Italian", "Japanese", "Vegetarian", "Spanish", "Seafood"],
        "activities": ["museum", "sightseeing", "shopping", "cooking class", "wine tasting", "cycling"],
        "language": "English",
        "currency": "EUR",
        "seat_preference": "aisle",
        "room_preference": "high floor, non-smoking",
        "newsletter_opt_in": True
    },
    "loyalty_programs": ["Marriott Bonvoy", "SkyTeam", "Accor Live Limitless"],
    "frequent_flyer_numbers": {"SkyTeam": "SKY123456", "British Airways": "BA987654"},
    "special_needs": {"mobility": False, "diet": "vegetarian", "allergies": ["peanuts"]},
    "last_search": {"destination": "Barcelona", "date": "2025-06-15", "guests": 2, "nights": 5, "room_type": "deluxe"},
    "saved_trips": [
        {"destination": "Santorini", "dates": ["2025-09-10", "2025-09-17"], "guests": 2, "notes": "Anniversary trip, prefer sea view room."},
        {"destination": "New York", "dates": ["2026-04-01", "2026-04-10"], "guests": 1, "notes": "Business conference, need airport transfer."}
    ],
    "recent_activity": [
        {"type": "search", "query": "best vegan restaurants in Barcelona", "timestamp": "2025-07-01T10:15:00"},
        {"type": "booking", "item": "flight", "details": {"from": "London", "to": "Barcelona", "date": "2025-06-15"}, "timestamp": "2025-05-20T14:30:00"},
        {"type": "review", "item": "hotel", "destination": "Paris", "rating": 4.5, "comment": "Great location and breakfast."}
    ],
    "emergency_contacts": [
        {"name": "John Smith", "relation": "spouse", "phone": "+44 7911 654321"},
        {"name": "Mary Smith", "relation": "mother", "phone": "+44 7911 111222"}
    ],
    "settings": {
        "language": "en-GB",
        "timezone": "Europe/London",
        "dark_mode": True,
        "voice_assistant": True
    }
}
