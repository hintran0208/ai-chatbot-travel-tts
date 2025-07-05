# TravelBot Use Cases: Step-by-Step Function Calling Scenarios

*See also: [README.md](README.md), [PROMPT_ENGINEERING.md](PROMPT_ENGINEERING.md), and [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for more details.*

This document provides detailed, step-by-step use cases for TravelBot, including user prompts, assistant logic, function call inputs/outputs, and the final assistant response. Each use case demonstrates how the assistant orchestrates multiple function calls to fulfill complex travel planning requests.

---

## Use Case 1: 1-Week Trip Plan to Paris
**User Prompt:**

> Plan a 1-week trip to Paris for me.

**Step-by-Step Logic:**
1. Parse the destination (Paris) and duration (1 week).
2. Determine check-in/check-out dates (e.g., today + 7 days).
3. Search for hotels in Paris for the specified dates.
4. Suggest top local activities in Paris.
5. Check the weather forecast for Paris during the trip.
6. Present a combined itinerary with hotel, activities, and weather info.

**API Called via Function Call:**
- `search_hotels`
  - Input: `{ "destination": "Paris", "check_in": "2025-06-28", "check_out": "2025-07-05", "guests": 1 }`
  - Output: `{ "destination": "Paris", "check_in": "2025-06-28", "check_out": "2025-07-05", "guests": 1, "hotels": [{"name": "Grand Paris Hotel", "price": 220, "rating": 4.7, "amenities": ["WiFi", "Pool", "Gym", "Restaurant"], "location": "Downtown Paris"}]}`
- `get_local_activities`
  - Input: `{ "destination": "Paris", "activity_type": "all" }`
  - Output: `{ "destination": "Paris", "activities": [{"name": "Paris Art Museum", "category": "cultural", "price": 20, "duration": "2-3 hours"}, {"name": "Seine River Cruise", "category": "adventure", "price": 40, "duration": "2 hours"}]}`
- `get_weather`
  - Input: `{ "city": "Paris", "date": "2025-06-28" }`
  - Output: `{ "city": "Paris", "date": "2025-06-28", "temperature": {"high": 27, "low": 16, "current": 22}, "condition": "Sunny", "humidity": 55, "wind_speed": 6.0, "visibility": 10}`

**Response from Assistant:**

### 🗓️ 1-Week Paris Trip Plan

#### 🏨 Hotel Recommendation
**Grand Paris Hotel**
- Price: $220/night
- Rating: 4.7
- Amenities: WiFi, Pool, Gym, Restaurant
- Location: Downtown Paris

#### 🎭 Top Activities
- **Paris Art Museum** (Cultural): $20, 2-3 hours
- **Seine River Cruise** (Adventure): $40, 2 hours

#### 🌤️ Weather Forecast (2025-06-28)
- Sunny, High: 27°C, Low: 16°C, Current: 22°C
- Humidity: 55%, Wind: 6.0 km/h

Would you like to see more hotel options, add flights, or customize your itinerary?

---

## Use Case 2: Find Flights and Convert Currency
**User Prompt:**

> Find me a flight from New York to Tokyo on December 15th and show the price in VND.

**Step-by-Step Logic:**
1. Parse origin (New York), destination (Tokyo), and date (December 15th).
2. Search for flights for the specified route and date.
3. Convert the price of the top flight from USD to VND.
4. Present flight options with prices in both USD and VND.

**API Called via Function Call:**
- `search_flights`
  - Input: `{ "origin": "NYC", "destination": "TYO", "departure_date": "2025-12-15" }`
  - Output: `{ "origin": "NYC", "destination": "TYO", "departure_date": "2025-12-15", "outbound_flights": [{"airline": "SkyWings Airlines", "flight_number": "SK123", "departure_time": "08:00", "arrival_time": "16:00", "price": 800, "duration": "14h 0m", "stops": 1}]}`
- `exchange_currency`
  - Input: `{ "amount": 800, "from_currency": "USD", "to_currency": "VND" }`
  - Output: `{ "source": "ExchangeRate-API.com", "amount": 800, "from_currency": "USD", "to_currency": "VND", "rate": 24500.0, "exchanged_amount": 19600000.0, "last_update": "2025-06-28T12:00:00Z"}`

**Response from Assistant:**

### ✈️ Flight Options from New York to Tokyo (2025-12-15)
1. **SkyWings Airlines SK123**
   - Departure: 08:00
   - Arrival: 16:00
   - Price: $800 (≈ 19,600,000 VND)
   - Duration: 14h 0m
   - Stops: 1

*Exchange rate: 1 USD = 24,500 VND (as of 2025-06-28)*

---

## Use Case 3: Suggest Activities and Check Weather
**User Prompt:**

> What are some food activities in Barcelona next weekend? Also, what's the weather like?

**Step-by-Step Logic:**
1. Parse destination (Barcelona), activity type (food), and date (next weekend).
2. Search for food activities in Barcelona.
3. Check the weather forecast for Barcelona on the specified date.
4. Present activities and weather info together.

**API Called via Function Call:**
- `get_local_activities`
  - Input: `{ "destination": "Barcelona", "activity_type": "food" }`
  - Output: `{ "destination": "Barcelona", "activity_type": "food", "activities": [{"name": "Barcelona Food Tour", "category": "food", "price": 60, "duration": "4 hours"}, {"name": "Cooking Class in Barcelona", "category": "food", "price": 90, "duration": "3 hours"}]}`
- `get_weather`
  - Input: `{ "city": "Barcelona", "date": "2025-07-05" }`
  - Output: `{ "city": "Barcelona", "date": "2025-07-05", "temperature": {"high": 30, "low": 20, "current": 25}, "condition": "Sunny", "humidity": 50, "wind_speed": 7.0, "visibility": 10}`

**Response from Assistant:**

### 🍽️ Food Activities in Barcelona (2025-07-05)
- **Barcelona Food Tour**: $60, 4 hours
- **Cooking Class in Barcelona**: $90, 3 hours

### 🌤️ Weather Forecast
- Sunny, High: 30°C, Low: 20°C, Current: 25°C
- Humidity: 50%, Wind: 7.0 km/h

---

## Use Case 4: Round-Trip Flight and Hotel Package
**User Prompt:**

> Book a round-trip flight from Los Angeles to Rome for 2 people, leaving July 10th and returning July 20th, and suggest a hotel.

**Step-by-Step Logic:**
1. Parse origin (Los Angeles), destination (Rome), departure/return dates, and number of guests (2).
2. Search for round-trip flights for the specified route and dates.
3. Search for hotels in Rome for the same dates and 2 guests.
4. Present flight and hotel options together.

**API Called via Function Call:**
- `search_flights`
  - Input: `{ "origin": "LAX", "destination": "ROM", "departure_date": "2025-07-10", "return_date": "2025-07-20" }`
  - Output: `{ "origin": "LAX", "destination": "ROM", "departure_date": "2025-07-10", "outbound_flights": [{"airline": "JetStream Airways", "flight_number": "JS789", "departure_time": "09:00", "arrival_time": "17:00", "price": 950, "duration": "11h 0m", "stops": 1}], "return_date": "2025-07-20", "return_flights": [{"airline": "Pacific Express", "flight_number": "PE321", "departure_time": "12:00", "arrival_time": "20:00", "price": 970, "duration": "11h 0m", "stops": 1}]}`
- `search_hotels`
  - Input: `{ "destination": "Rome", "check_in": "2025-07-10", "check_out": "2025-07-20", "guests": 2 }`
  - Output: `{ "destination": "Rome", "check_in": "2025-07-10", "check_out": "2025-07-20", "guests": 2, "hotels": [{"name": "Grand Rome Hotel", "price": 210, "rating": 4.6, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"], "location": "Central Rome"}]}`

**Response from Assistant:**

### ✈️ Round-Trip Flight Options (LAX → ROM, 2025-07-10 to 2025-07-20)
1. **JetStream Airways JS789**
   - Departure: 09:00
   - Arrival: 17:00
   - Price: $950
   - Duration: 11h 0m
   - Stops: 1

### ✈️ Return Flight
1. **Pacific Express PE321**
   - Departure: 12:00
   - Arrival: 20:00
   - Price: $970
   - Duration: 11h 0m
   - Stops: 1

### 🏨 Hotel Suggestion
**Grand Rome Hotel**
- Price: $210/night
- Rating: 4.6
- Amenities: WiFi, Pool, Spa, Restaurant
- Location: Central Rome

---

## Use Case 5: Currency Conversion for Activities
**User Prompt:**

> How much would a $50 food tour in Barcelona cost in EUR?

**Step-by-Step Logic:**
1. Parse the amount (50), source currency (USD), and target currency (EUR).
2. Convert the amount using the latest exchange rate.
3. Present the converted price.

**API Called via Function Call:**
- `exchange_currency`
  - Input: `{ "amount": 50, "from_currency": "USD", "to_currency": "EUR" }`
  - Output: `{ "source": "ExchangeRate-API.com", "amount": 50, "from_currency": "USD", "to_currency": "EUR", "rate": 0.92, "exchanged_amount": 46.0, "last_update": "2025-06-28T12:00:00Z"}`

**Response from Assistant:**

**Currency Conversion**
- $50 USD ≈ €46.00 (Rate: 0.92)
- Last update: 2025-06-28T12:00:00Z

---

## Use Case 6: Multi-City Itinerary (Batching)
**User Prompt:**

> Plan a 5-day trip: 2 days in Rome, 3 days in Florence. Suggest hotels and activities for both cities.

**Step-by-Step Logic:**
1. Parse cities (Rome, Florence) and durations (2 days, 3 days).
2. For each city:
   - Search for hotels for the specified dates.
   - Suggest top activities.
3. Present a combined itinerary for both cities.

**API Called via Function Call:**
- `search_hotels` (Rome)
  - Input: `{ "destination": "Rome", "check_in": "2025-07-01", "check_out": "2025-07-03", "guests": 1 }`
  - Output: `{ "destination": "Rome", "check_in": "2025-07-01", "check_out": "2025-07-03", "guests": 1, "hotels": [{"name": "Rome Central Hotel", "price": 180, "rating": 4.5, "amenities": ["WiFi", "Breakfast"], "location": "Rome Center"}]}`
- `get_local_activities` (Rome)
  - Input: `{ "destination": "Rome", "activity_type": "all" }`
  - Output: `{ "destination": "Rome", "activities": [{"name": "Colosseum Tour", "category": "cultural", "price": 30, "duration": "3 hours"}]}`
- `search_hotels` (Florence)
  - Input: `{ "destination": "Florence", "check_in": "2025-07-03", "check_out": "2025-07-06", "guests": 1 }`
  - Output: `{ "destination": "Florence", "check_in": "2025-07-03", "check_out": "2025-07-06", "guests": 1, "hotels": [{"name": "Florence Art Hotel", "price": 160, "rating": 4.4, "amenities": ["WiFi", "Breakfast"], "location": "Florence Center"}]}`
- `get_local_activities` (Florence)
  - Input: `{ "destination": "Florence", "activity_type": "all" }`
  - Output: `{ "destination": "Florence", "activities": [{"name": "Uffizi Gallery Tour", "category": "cultural", "price": 25, "duration": "2 hours"}]}`

**Response from Assistant:**

### 🗺️ 5-Day Multi-City Itinerary

#### Rome (2 days)
- **Hotel:** Rome Central Hotel ($180/night, 4.5⭐, WiFi, Breakfast)
- **Activity:** Colosseum Tour ($30, 3 hours)

#### Florence (3 days)
- **Hotel:** Florence Art Hotel ($160/night, 4.4⭐, WiFi, Breakfast)
- **Activity:** Uffizi Gallery Tour ($25, 2 hours)

---

## Use Case 7: Exporting a Travel Plan to Excel or TXT
**User Prompt:**

> Export my Paris trip itinerary as an Excel file.

**Step-by-Step Logic:**
1. User requests to export a specific travel plan (e.g., Paris trip) and selects the desired format (Excel or TXT).
2. The assistant gathers the relevant itinerary details (hotels, flights, activities, weather, etc.).
3. The assistant calls the export endpoint with the itinerary data and chosen format.
4. The backend generates the file (Excel or TXT) and returns it as a downloadable response.

**API Called via Function Call:**
- `/api/export` (POST)
    - Input: `{ "itinerary": { "destination": "Paris", "dates": ["2025-06-28", "2025-07-05"], "hotel": {...}, "activities": [...], "weather": {...} }, "format": "excel", "filename": "paris_trip_20250628.xlsx" }`
    - Output: (Excel file stream)
- `/api/export` (POST)
    - Input: `{ "itinerary": { "destination": "Paris", "dates": ["2025-06-28", "2025-07-05"], "hotel": {...}, "activities": [...], "weather": {...} }, "format": "txt", "filename": "paris_trip_20250628.txt" }`
    - Output: (TXT file stream)

**Response from Assistant:**

> Your Paris trip itinerary is ready for download:
> - [Download Excel file](#)
> - [Download TXT file](#)

---

Each use case demonstrates how TravelBot combines multiple function calls and real-time data to deliver a comprehensive, context-aware travel planning experience.
