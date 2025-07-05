# knowledge/travel_knowledge.py

"""
Travel knowledge base mock data for Travel Assistant Chatbot
"""

travel_knowledge = [
    # General Travel Tips
    {
        "title": "Best Time to Visit Europe",
        "content": "Spring (April-May) and Fall (September-October) offer mild weather and fewer crowds. Summer is peak season with higher prices but best weather. Winter is great for Christmas markets and skiing in the Alps.",
        "category": "travel_tips",
        "region": "Europe"
    },
    {
        "title": "Budget Travel Tips",
        "content": "Book flights in advance, use public transport, stay in hostels or budget hotels, eat like a local, use city tourist cards, and take advantage of free attractions and walking tours.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Packing Essentials",
        "content": "Pack light, bring versatile clothing, essential documents, first aid kit, portable charger, universal adapter, reusable water bottle, and comfortable walking shoes. Always check weather and local customs before packing.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Travel Insurance Advice",
        "content": "Always purchase travel insurance covering medical emergencies, trip cancellations, lost luggage, and personal liability. Compare policies and read the fine print for exclusions.",
        "category": "safety",
        "region": "global"
    },
    # Accommodation
    {
        "title": "Hotel Booking Tips",
        "content": "Compare prices across platforms, read recent reviews, check cancellation policies, book directly with hotels for better rates, and consider location vs price. Use loyalty programs for extra perks.",
        "category": "accommodation",
        "region": "global"
    },
    {
        "title": "Alternative Accommodation Options",
        "content": "Consider vacation rentals (Airbnb, Vrbo), hostels, guesthouses, boutique hotels, and homestays for unique experiences and potential savings.",
        "category": "accommodation",
        "region": "global"
    },
    # Transportation
    {
        "title": "Flight Booking Strategies",
        "content": "Use flexible date searches, clear browser cookies, compare one-way vs round-trip, consider layovers, and book Tuesday-Thursday for better prices. Use flight comparison tools like Skyscanner and Google Flights.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Train Travel in Europe",
        "content": "Eurail and Interrail passes offer flexible train travel across Europe. Book high-speed trains in advance for best prices. Night trains can save on accommodation costs.",
        "category": "transportation",
        "region": "Europe"
    },
    {
        "title": "Public Transport Tips",
        "content": "Purchase city transport cards for unlimited rides, use apps for real-time schedules, and always validate your ticket. In some cities, cycling or e-scooters are convenient options.",
        "category": "transportation",
        "region": "global"
    },
    # Destinations & Activities
    {
        "title": "Southeast Asia Travel Guide",
        "content": "Visit during dry season (November-April), try street food, respect local customs, negotiate prices, and carry cash for smaller vendors. Top destinations: Thailand, Vietnam, Cambodia, Indonesia.",
        "category": "destination_guide",
        "region": "Southeast Asia"
    },
    {
        "title": "Top Adventure Activities Worldwide",
        "content": "Popular adventure activities include hiking in Patagonia, scuba diving in the Great Barrier Reef, safari in Africa, skiing in the Alps, and ziplining in Costa Rica.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Cultural Etiquette in Japan",
        "content": "Bow when greeting, remove shoes indoors, avoid loud conversations in public, never stick chopsticks upright in rice, and always be punctual.",
        "category": "culture",
        "region": "Japan"
    },
    {
        "title": "Must-Try Foods in Italy",
        "content": "Sample pizza in Naples, pasta in Rome, gelato everywhere, and regional specialties like risotto in Milan and seafood in Sicily.",
        "category": "food",
        "region": "Italy"
    },
    # Money & Currency
    {
        "title": "Currency Exchange Tips",
        "content": "Use ATMs for the best rates, avoid airport exchange counters, notify your bank before travel, and carry a small amount of local cash for emergencies.",
        "category": "money",
        "region": "global"
    },
    {
        "title": "Tipping Practices Around the World",
        "content": "Tipping is expected in the US (15-20%), optional in Japan, and included in bills in many European countries. Always check local customs before tipping.",
        "category": "money",
        "region": "global"
    },
    # Safety & Health
    {
        "title": "Emergency Travel Tips",
        "content": "Keep copies of important documents, know embassy contact info, have travel insurance, keep emergency cash hidden, and register with your embassy. Learn basic local emergency numbers.",
        "category": "safety",
        "region": "global"
    },
    {
        "title": "Staying Healthy While Traveling",
        "content": "Drink bottled water where tap water isn't safe, wash hands frequently, use insect repellent in tropical areas, and check vaccination requirements before departure.",
        "category": "health",
        "region": "global"
    },
    # Technology & Connectivity
    {
        "title": "Staying Connected Abroad",
        "content": "Buy a local SIM card or eSIM for affordable data, use Wi-Fi calling apps, and download offline maps. Consider portable Wi-Fi devices for group travel.",
        "category": "technology",
        "region": "global"
    },
    # Family & Accessibility
    {
        "title": "Traveling with Children",
        "content": "Plan for frequent breaks, bring snacks and entertainment, choose family-friendly accommodations, and check for child discounts on transport and attractions.",
        "category": "family",
        "region": "global"
    },
    {
        "title": "Accessible Travel Tips",
        "content": "Research accessible hotels and attractions, notify airlines of special needs in advance, and use resources like AccessibleGO and Wheelmap for planning.",
        "category": "accessibility",
        "region": "global"
    },
    # Sustainable & Responsible Travel
    {
        "title": "Eco-Friendly Travel Tips",
        "content": "Reduce plastic use, choose eco-certified hotels, use public transport, support local businesses, and respect wildlife and natural habitats.",
        "category": "sustainability",
        "region": "global"
    },
    {
        "title": "Voluntourism Advice",
        "content": "Research organizations carefully, ensure your work is ethical and sustainable, and prioritize projects that benefit local communities.",
        "category": "sustainability",
        "region": "global"
    },
    # Business Travel
    {
        "title": "Business Travel Essentials",
        "content": "Pack business attire, bring backup chargers, keep digital and paper copies of important documents, and use travel apps to manage itineraries and expenses.",
        "category": "business",
        "region": "global"
    },
    # LGBTQ+ Travel
    {
        "title": "LGBTQ+ Travel Safety Tips",
        "content": "Research local laws and customs, connect with LGBTQ+ travel groups, choose inclusive accommodations, and use resources like Equaldex for destination info.",
        "category": "lgbtq",
        "region": "global"
    },
    # Pet Travel
    {
        "title": "Traveling with Pets",
        "content": "Check airline pet policies, ensure vaccinations are up to date, bring familiar items for comfort, and research pet-friendly accommodations and parks.",
        "category": "pets",
        "region": "global"
    },
    # --- Additional Mock Knowledge Base Entries ---
    {
        "title": "Best Beaches in Southeast Asia",
        "content": "Explore pristine beaches like White Beach in Boracay, Philippines; Railay Beach in Thailand; and Nha Trang in Vietnam for sunbathing, snorkeling, and water sports.",
        "category": "destination_guide",
        "region": "Southeast Asia"
    },
    {
        "title": "Visa Requirements for Schengen Area",
        "content": "Most non-EU travelers need a Schengen visa to visit 26 European countries. Apply in advance, provide proof of accommodation, travel insurance, and sufficient funds.",
        "category": "visa",
        "region": "Europe"
    },
    {
        "title": "Top Festivals in India",
        "content": "Experience Holi (Festival of Colors), Diwali (Festival of Lights), and Pushkar Camel Fair for vibrant cultural celebrations across India.",
        "category": "events",
        "region": "India"
    },
    {
        "title": "Traveling During Ramadan in the Middle East",
        "content": "Many restaurants close during daylight hours. Be respectful, avoid eating in public, and enjoy special evening meals (iftar) and cultural events.",
        "category": "culture",
        "region": "Middle East"
    },
    {
        "title": "Best Hiking Trails in North America",
        "content": "Try the Appalachian Trail (USA), West Coast Trail (Canada), and Zion Narrows (USA) for breathtaking scenery and adventure.",
        "category": "activities",
        "region": "North America"
    },
    {
        "title": "Traveling with Dietary Restrictions",
        "content": "Learn key phrases in the local language, carry allergy cards, research restaurants in advance, and use apps like HappyCow for vegetarian/vegan options.",
        "category": "health",
        "region": "global"
    },
    {
        "title": "Best Ski Resorts in Europe",
        "content": "Top resorts include Chamonix (France), Zermatt (Switzerland), and Cortina d'Ampezzo (Italy) for world-class skiing and après-ski activities.",
        "category": "activities",
        "region": "Europe"
    },
    {
        "title": "Travel Photography Tips",
        "content": "Use natural light, wake up early for golden hour, ask permission before photographing people, and back up your photos regularly.",
        "category": "technology",
        "region": "global"
    },
    {
        "title": "Traveling Solo as a Woman",
        "content": "Research destinations, stay in well-reviewed accommodations, trust your instincts, avoid walking alone at night, and keep family informed of your plans.",
        "category": "safety",
        "region": "global"
    },
    {
        "title": "Best Road Trips in Australia",
        "content": "Drive the Great Ocean Road, Pacific Coast, and Red Centre Way for stunning landscapes, wildlife, and unique outback experiences.",
        "category": "activities",
        "region": "Australia"
    },
    {
        "title": "Traveling with Disabilities in Europe",
        "content": "Many European cities offer accessible public transport, hotels, and attractions. Research accessibility in advance and use resources like AccessAble.",
        "category": "accessibility",
        "region": "Europe"
    },
    {
        "title": "Best Places for Wildlife Safaris",
        "content": "Visit Serengeti (Tanzania), Maasai Mara (Kenya), and Kruger National Park (South Africa) for unforgettable wildlife encounters.",
        "category": "activities",
        "region": "Africa"
    },
    {
        "title": "Traveling During the COVID-19 Pandemic",
        "content": "Check entry requirements, vaccination and testing rules, mask mandates, and quarantine policies before booking. Stay updated as regulations change frequently.",
        "category": "health",
        "region": "global"
    },
    {
        "title": "Best Cities for Digital Nomads",
        "content": "Top cities include Bali (Indonesia), Chiang Mai (Thailand), Lisbon (Portugal), and Medellín (Colombia) for coworking spaces, affordability, and expat communities.",
        "category": "technology",
        "region": "global"
    },
    {
        "title": "Traveling with Large Groups",
        "content": "Book accommodations early, use group messaging apps, assign roles, and plan flexible itineraries to accommodate different interests.",
        "category": "family",
        "region": "global"
    },
    {
        "title": "Best Cruise Destinations",
        "content": "Popular cruise routes include the Caribbean, Mediterranean, Alaska, and Norwegian fjords. Consider themed cruises for unique experiences.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Traveling with Infants and Toddlers",
        "content": "Bring familiar toys, snacks, and comfort items. Choose direct flights, request bassinets, and plan for extra time at airports.",
        "category": "family",
        "region": "global"
    },
    {
        "title": "Best Places to See the Northern Lights",
        "content": "Visit Tromsø (Norway), Reykjavik (Iceland), and Fairbanks (Alaska) between September and March for the best aurora viewing.",
        "category": "destination_guide",
        "region": "Arctic"
    },
    {
        "title": "Traveling with Medication",
        "content": "Carry prescriptions in original packaging, bring a doctor's note, check regulations for controlled substances, and pack extra in case of delays.",
        "category": "health",
        "region": "global"
    },
    {
        "title": "Best Food Markets Around the World",
        "content": "Explore Borough Market (London), Tsukiji Market (Tokyo), La Boqueria (Barcelona), and Chatuchak Market (Bangkok) for local flavors and culture.",
        "category": "food",
        "region": "global"
    },
    {
        "title": "Traveling During High Season",
        "content": "Book accommodations and activities well in advance, expect crowds, and consider visiting popular sites early in the morning or late afternoon.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best UNESCO World Heritage Sites",
        "content": "Don't miss Machu Picchu (Peru), Angkor Wat (Cambodia), Great Wall of China, and Petra (Jordan) for history and culture.",
        "category": "destination_guide",
        "region": "global"
    },
    {
        "title": "Traveling with Electronics",
        "content": "Bring universal adapters, power banks, surge protectors, and check voltage compatibility. Download offline maps and entertainment for long journeys.",
        "category": "technology",
        "region": "global"
    },
    {
        "title": "Best Places for Scuba Diving",
        "content": "Top dive spots include the Great Barrier Reef (Australia), Blue Hole (Belize), and Red Sea (Egypt) for vibrant marine life and clear waters.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with Allergies",
        "content": "Carry allergy medication, inform airlines and hotels in advance, and use translation cards to communicate dietary needs.",
        "category": "health",
        "region": "global"
    },
    {
        "title": "Best Cities for Street Food",
        "content": "Bangkok, Mexico City, Istanbul, and Marrakech are famous for delicious and affordable street food. Try local specialties and follow the crowds for the best vendors.",
        "category": "food",
        "region": "global"
    },
    {
        "title": "Traveling with Seniors",
        "content": "Choose destinations with good healthcare, accessible transport, and comfortable accommodations. Plan for slower-paced itineraries and regular rest stops.",
        "category": "family",
        "region": "global"
    },
    {
        "title": "Best Places for Wine Tourism",
        "content": "Visit Napa Valley (USA), Bordeaux (France), Tuscany (Italy), and Mendoza (Argentina) for vineyard tours, tastings, and scenic landscapes.",
        "category": "food",
        "region": "global"
    },
    {
        "title": "Traveling with a Tight Budget",
        "content": "Use overnight buses or trains, cook your own meals, travel during shoulder season, and look for free walking tours and museum days.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best Destinations for Wildlife Watching",
        "content": "See gorillas in Rwanda, orangutans in Borneo, whales in Iceland, and penguins in Antarctica for unforgettable wildlife experiences.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Language Barrier",
        "content": "Learn basic phrases, use translation apps, carry a phrasebook, and use gestures and pictures to communicate when needed.",
        "category": "culture",
        "region": "global"
    },
    {
        "title": "Best Cities for Art Lovers",
        "content": "Paris, Florence, New York, and St. Petersburg are home to world-class museums, galleries, and public art installations.",
        "category": "culture",
        "region": "global"
    },
    {
        "title": "Traveling with a Drone",
        "content": "Check local regulations, register your drone if required, avoid flying near airports or crowds, and respect privacy and no-fly zones.",
        "category": "technology",
        "region": "global"
    },
    {
        "title": "Best Places for Stargazing",
        "content": "Visit Atacama Desert (Chile), Mauna Kea (Hawaii), and Jasper National Park (Canada) for clear skies and minimal light pollution.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Service Animal",
        "content": "Check airline and accommodation policies, carry documentation, and ensure your animal is trained for travel environments.",
        "category": "accessibility",
        "region": "global"
    },
    {
        "title": "Best Destinations for History Buffs",
        "content": "Explore Rome, Athens, Cairo, and Beijing for ancient ruins, museums, and guided history tours.",
        "category": "destination_guide",
        "region": "global"
    },
    {
        "title": "Traveling with a Rental Car",
        "content": "Check license requirements, insurance coverage, and local driving laws. Inspect the car before departure and use GPS or offline maps.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Best Places for Mountain Climbing",
        "content": "Climb Mount Kilimanjaro (Tanzania), Mont Blanc (France/Italy), and Mount Fuji (Japan) for challenging and scenic ascents.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Backpack",
        "content": "Choose a comfortable, lightweight backpack, pack only essentials, and use packing cubes for organization. Secure valuables in hidden pockets.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best Cities for Nightlife",
        "content": "Berlin, Las Vegas, Rio de Janeiro, and Bangkok are renowned for vibrant nightlife, clubs, and live music venues.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Bicycle",
        "content": "Research bike-friendly cities, pack a repair kit, use bike-sharing programs, and follow local traffic rules for cyclists.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Best Places for Hot Air Balloon Rides",
        "content": "Experience Cappadocia (Turkey), Albuquerque (USA), and Bagan (Myanmar) for breathtaking hot air balloon adventures.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Tight Schedule",
        "content": "Prioritize must-see attractions, book skip-the-line tickets, use express transport options, and plan rest breaks to avoid burnout.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best Destinations for Foodies",
        "content": "Visit Tokyo, Paris, Bangkok, and New Orleans for world-class cuisine, street food, and culinary tours.",
        "category": "food",
        "region": "global"
    },
    {
        "title": "Traveling with a Cruise Ship",
        "content": "Pack formal and casual attire, book shore excursions early, and check onboard amenities and dining options before departure.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Best Places for Whale Watching",
        "content": "Go to Hermanus (South Africa), Husavik (Iceland), and Monterey Bay (USA) for seasonal whale watching tours.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Student Budget",
        "content": "Use student discounts, stay in hostels, travel off-peak, and use ISIC cards for savings on transport and attractions.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best Cities for Shopping",
        "content": "Shop in Milan, Dubai, New York, and Hong Kong for luxury brands, local markets, and unique souvenirs.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Campervan",
        "content": "Plan your route, book campsites in advance, pack cooking gear, and follow local camping regulations for a safe and enjoyable trip.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Best Places for Birdwatching",
        "content": "Visit Costa Rica, South Africa, and Australia for diverse bird species and guided birdwatching tours.",
        "category": "activities",
        "region": "global"
    },
    {
        "title": "Traveling with a Group Tour",
        "content": "Choose reputable tour operators, read reviews, clarify what's included, and communicate preferences with your guide.",
        "category": "travel_tips",
        "region": "global"
    },
    {
        "title": "Best Destinations for Honeymoons",
        "content": "Consider Maldives, Bora Bora, Santorini, and Maui for romantic resorts, private beaches, and luxury experiences.",
        "category": "destination_guide",
        "region": "global"
    },
    {
        "title": "Traveling with a Tight Connection",
        "content": "Book flights with sufficient layover time, check terminal maps, and use priority security lines if available.",
        "category": "transportation",
        "region": "global"
    },
    {
        "title": "Best Places for Desert Adventures",
        "content": "Explore Sahara (Morocco), Atacama (Chile), and Wadi Rum (Jordan) for camel treks, stargazing, and sandboarding.",
        "category": "activities",
        "region": "global"
    }
]
