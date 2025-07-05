"""
Travel Assistant Chatbot using OpenAI SDK

Advanced travel chatbot with function calling, external API integrations,
and real-time conversation management for comprehensive travel assistance.
"""

import os
import json
import uuid
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import uvicorn
import httpx
import random
import pandas as pd
import openpyxl
from io import BytesIO, StringIO
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import torch
from transformers import VitsModel, AutoTokenizer
import numpy as np
import base64
import soundfile as sf
import tempfile
import librosa
from scipy.io import wavfile
import warnings
from knowledge.travel_knowledge import travel_knowledge
from knowledge.user_mock_data import user_mock_data
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# FastAPI app initialization
app = FastAPI(
    title="Travel Assistant Chatbot",
    description="AI-powered travel assistant with real-time chat, hotel booking, flight search, and weather information",
    version="2.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

# Create templates and static directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Text-to-Speech Setup
tts_model = None
tts_tokenizer = None

def initialize_tts():
    """Initialize TTS model (lazy loading)"""
    global tts_model, tts_tokenizer
    try:
        if tts_model is None:
            print("🔊 Initializing Text-to-Speech model...")
            tts_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
            tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
            print("✅ TTS model initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing TTS: {e}")
        print("TTS functionality will be disabled")

def text_to_speech(text: str, max_length: int = 200, speed: float = 1.0) -> Optional[str]:
    """Convert text to speech and return base64 encoded audio with speed control"""
    try:
        if tts_model is None or tts_tokenizer is None:
            print("TTS model not initialized")
            return None
        
        # Truncate text if too long
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Tokenize and generate speech
        inputs = tts_tokenizer(text, return_tensors="pt")
        
        with torch.no_grad():
            output = tts_model(**inputs).waveform
        
        # Convert to numpy array and normalize
        waveform = output.squeeze().cpu().numpy()
        
        # Apply speed adjustment if needed
        if speed != 1.0:
            # Clamp speed to reasonable range
            speed = max(0.5, min(2.0, speed))
            
            # Use librosa for time stretching (speed adjustment)
            waveform = librosa.effects.time_stretch(waveform, rate=speed)
        
        # Use BytesIO instead of temporary file to avoid file access issues
        audio_buffer = BytesIO()
        
        # Write audio to buffer
        sf.write(audio_buffer, waveform, 16000, format='WAV')
        
        # Get audio data from buffer
        audio_buffer.seek(0)
        audio_data = audio_buffer.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Close buffer
        audio_buffer.close()
        
        return audio_base64
    
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

# OpenAI Client Setup
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://aiportalapi.stu-platform.live/jpe"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = os.getenv("OPENAI_MODEL_NAME", "GPT-4o-mini")

# ChromaDB Setup for Vector Storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Initialize OpenAI embedding function for ChromaDB
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY_EMBEDDING"),
    model_name="text-embedding-3-small"
)

# Create or get collections
try:
    user_conversations_collection = chroma_client.create_collection(
        name="user_conversations",
        embedding_function=openai_ef,
        metadata={"description": "User conversation history and preferences"}
    )
except Exception:
    user_conversations_collection = chroma_client.get_collection(
        name="user_conversations",
        embedding_function=openai_ef
    )

try:
    travel_knowledge_collection = chroma_client.create_collection(
        name="travel_knowledge",
        embedding_function=openai_ef,
        metadata={"description": "Travel knowledge base and tips"}
    )
except Exception:
    travel_knowledge_collection = chroma_client.get_collection(
        name="travel_knowledge",
        embedding_function=openai_ef
    )

# Initialize Travel Knowledge Base
async def initialize_travel_knowledge():
    """Initialize the travel knowledge base with predefined data"""
    try:
        # Check if knowledge base is already populated
        existing_count = travel_knowledge_collection.count()
        if existing_count > 0:
            print(f"Travel knowledge base already contains {existing_count} entries")
            return
        
        # Add travel knowledge to ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for i, knowledge in enumerate(travel_knowledge):
            doc_id = f"knowledge_{i}"
            documents.append(f"{knowledge['title']}: {knowledge['content']}")
            metadatas.append({
                "title": knowledge['title'],
                "category": knowledge['category'],
                "tags": ",".join(knowledge['tags'])
            })
            ids.append(doc_id)
        
        # Add to ChromaDB in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            travel_knowledge_collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
        
        print(f"Successfully initialized travel knowledge base with {len(documents)} entries")
        
    except Exception as e:
        print(f"Error initializing travel knowledge base: {e}")

# Initialize knowledge base on startup
async def startup_initialization():
    """Initialize the application on startup"""
    initialize_tts()
    await initialize_travel_knowledge()

# Initialize knowledge base on startup when the app starts
@app.on_event("startup")
async def on_startup():
    await startup_initialization()

# In-memory storage for active conversations
conversations: Dict[str, List[Dict]] = {}

# Connection manager for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_conversations: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Generate unique conversation ID for this connection
        conversation_id = str(uuid.uuid4())
        self.connection_conversations[websocket] = conversation_id
        return conversation_id

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_conversations:
            del self.connection_conversations[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# Data Models
class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    personalized: bool = Field(default=False, description="Whether to use personalized responses")
    speech_speed: float = Field(default=1.0, description="Speech speed for TTS (0.5-2.0)")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI's response")
    conversation_id: str = Field(..., description="The conversation ID")
    function_calls: List[Dict] = Field(default_factory=list, description="Function calls made")
    audio_base64: Optional[str] = Field(None, description="Base64 encoded audio response")

class ExportRequest(BaseModel):
    messages: List[Dict[str, Any]] = Field(..., description="Messages to export")
    format: str = Field(..., description="Export format: 'excel' or 'txt'")
    filename: Optional[str] = Field(None, description="Optional filename")

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    speed: float = Field(1.0, description="Speech speed multiplier (0.5-2.0, default: 1.0)")
    max_length: int = Field(200, description="Maximum text length (default: 200)")

# Weather API Functions
async def get_weather(city: str, country: str = "") -> Dict[str, Any]:
    """Get current weather information for a city"""
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return {"error": "Weather API key not configured"}
        
        query = f"{city},{country}" if country else city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
            else:
                return {"error": f"Weather data not found for {city}"}
    except Exception as e:
        return {"error": f"Error fetching weather: {str(e)}"}

async def get_forecast(city: str, country: str = "", days: int = 5) -> Dict[str, Any]:
    """Get weather forecast for a city"""
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return {"error": "Weather API key not configured"}
        
        query = f"{city},{country}" if country else city
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={query}&appid={api_key}&units=metric&cnt={days*8}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                for item in data["list"][::8]:  # Every 8th item (24 hours)
                    forecasts.append({
                        "date": item["dt_txt"].split(" ")[0],
                        "temperature": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "humidity": item["main"]["humidity"]
                    })
                return {
                    "city": data["city"]["name"],
                    "country": data["city"]["country"],
                    "forecasts": forecasts
                }
            else:
                return {"error": f"Forecast data not found for {city}"}
    except Exception as e:
        return {"error": f"Error fetching forecast: {str(e)}"}

# Travel Information Functions
async def search_flights(origin: str, destination: str, departure_date: str, return_date: str = None) -> Dict[str, Any]:
    """Search for flights between two cities"""
    try:
        # Mock flight search (replace with real API)
        flights = [
            {
                "airline": "Air Travel Plus",
                "flight_number": f"AT{random.randint(100, 999)}",
                "departure_time": "08:30",
                "arrival_time": "14:45",
                "price": random.randint(200, 800),
                "stops": random.choice([0, 1, 2]),
                "duration": f"{random.randint(2, 12)}h {random.randint(0, 59)}m"
            },
            {
                "airline": "Sky Connect",
                "flight_number": f"SC{random.randint(100, 999)}",
                "departure_time": "12:15",
                "arrival_time": "18:30",
                "price": random.randint(200, 800),
                "stops": random.choice([0, 1, 2]),
                "duration": f"{random.randint(2, 12)}h {random.randint(0, 59)}m"
            }
        ]
        
        return {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "flights": flights
        }
    except Exception as e:
        return {"error": f"Error searching flights: {str(e)}"}

async def search_hotels(city: str, check_in: str, check_out: str, guests: int = 2) -> Dict[str, Any]:
    """Search for hotels in a city"""
    try:
        # Mock hotel search (replace with real API)
        hotels = [
            {
                "name": "Grand Plaza Hotel",
                "rating": 4.5,
                "price_per_night": random.randint(80, 300),
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
                "location": "City Center",
                "availability": "Available"
            },
            {
                "name": "Comfort Inn & Suites",
                "rating": 4.2,
                "price_per_night": random.randint(60, 200),
                "amenities": ["WiFi", "Breakfast", "Gym", "Parking"],
                "location": "Downtown",
                "availability": "Available"
            },
            {
                "name": "Luxury Resort & Spa",
                "rating": 4.8,
                "price_per_night": random.randint(200, 500),
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Beach Access"],
                "location": "Beachfront",
                "availability": "Limited"
            }
        ]
        
        return {
            "city": city,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "hotels": hotels
        }
    except Exception as e:
        return {"error": f"Error searching hotels: {str(e)}"}

async def get_attractions(city: str, category: str = "all") -> Dict[str, Any]:
    """Get tourist attractions in a city"""
    try:
        # Mock attractions data (replace with real API)
        attractions = [
            {
                "name": "Historic Cathedral",
                "category": "historical",
                "rating": 4.6,
                "description": "Beautiful 12th-century cathedral with stunning architecture",
                "opening_hours": "9:00 AM - 6:00 PM",
                "admission_fee": "$10"
            },
            {
                "name": "City Art Museum",
                "category": "cultural",
                "rating": 4.4,
                "description": "Modern art museum featuring contemporary works",
                "opening_hours": "10:00 AM - 8:00 PM",
                "admission_fee": "$15"
            },
            {
                "name": "Central Park",
                "category": "nature",
                "rating": 4.7,
                "description": "Large urban park perfect for walking and picnics",
                "opening_hours": "24 hours",
                "admission_fee": "Free"
            }
        ]
        
        if category != "all":
            attractions = [attr for attr in attractions if attr["category"] == category]
        
        return {
            "city": city,
            "category": category,
            "attractions": attractions
        }
    except Exception as e:
        return {"error": f"Error getting attractions: {str(e)}"}

async def get_travel_tips(destination: str) -> Dict[str, Any]:
    """Get travel tips for a destination"""
    try:
        # Mock travel tips (replace with real data)
        tips = [
            {
                "category": "Transportation",
                "tip": "Use public transport cards for better rates"
            },
            {
                "category": "Safety",
                "tip": "Keep copies of important documents in separate locations"
            },
            {
                "category": "Culture",
                "tip": "Learn basic local phrases to enhance your experience"
            },
            {
                "category": "Money",
                "tip": "Notify your bank of travel plans to avoid card issues"
            }
        ]
        
        return {
            "destination": destination,
            "tips": tips
        }
    except Exception as e:
        return {"error": f"Error getting travel tips: {str(e)}"}

# Helper functions for ChromaDB integration
def get_relevant_conversation_history(query: str, conversation_id: str, limit: int = 3) -> List[Dict]:
    """Get relevant conversation history using vector search"""
    try:
        # Search for relevant conversations
        results = user_conversations_collection.query(
            query_texts=[query],
            n_results=limit,
            where={"conversation_id": conversation_id}
        )
        
        relevant_history = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                relevant_history.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return relevant_history
    except Exception as e:
        print(f"Error getting relevant conversation history: {e}")
        return []

def get_relevant_travel_knowledge(query: str, limit: int = 3) -> List[Dict]:
    """Get relevant travel knowledge using vector search"""
    try:
        # Search for relevant travel knowledge
        results = travel_knowledge_collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        relevant_knowledge = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                relevant_knowledge.append({
                    "title": metadata.get('title', 'Travel Tip'),
                    "content": doc,
                    "category": metadata.get('category', 'General'),
                    "tags": metadata.get('tags', '').split(',') if metadata.get('tags') else [],
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return relevant_knowledge
    except Exception as e:
        print(f"Error getting relevant travel knowledge: {e}")
        return []

def store_conversation(conversation_id: str, user_message: str, assistant_response: str):
    """Store conversation in ChromaDB for future reference"""
    try:
        # Create a document combining user message and assistant response
        document = f"User: {user_message}\nAssistant: {assistant_response}"
        
        # Add to ChromaDB
        user_conversations_collection.add(
            documents=[document],
            metadatas=[{
                "conversation_id": conversation_id,
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "assistant_response": assistant_response
            }],
            ids=[f"{conversation_id}_{datetime.now().timestamp()}"]
        )
    except Exception as e:
        print(f"Error storing conversation: {e}")

# Text-to-Speech Functions
def generate_speech_openai(text: str, voice: str = "alloy") -> Optional[str]:
    """Generate speech using OpenAI TTS (currently disabled due to API issues)"""
    try:
        # Temporarily disabled due to 404 errors
        print("OpenAI TTS temporarily disabled - using local TTS instead")
        return None
        
        # Original OpenAI TTS code (commented out)
        # response = client.audio.speech.create(
        #     model="tts-1",
        #     voice=voice,
        #     input=text,
        #     response_format="mp3"
        # )
        # 
        # # Convert to base64
        # audio_base64 = base64.b64encode(response.content).decode('utf-8')
        # return audio_base64
    except Exception as e:
        print(f"Error generating speech with OpenAI: {e}")
        return None

def generate_speech_vits(text: str, speech_speed: float = 1.0) -> Optional[str]:
    """Generate speech using VITS model with adjustable speed"""
    try:
        # Initialize VITS model (this is a placeholder - you'll need to implement actual VITS model)
        # For now, we'll use a simple audio generation approach
        
        # Create a simple tone as placeholder
        duration = len(text) * 0.1  # Rough estimate
        sample_rate = 22050
        frequency = 440  # A4 note
        
        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Adjust speed by resampling using librosa
        if speech_speed != 1.0:
            # Clamp speed to reasonable range
            speech_speed = max(0.5, min(2.0, speech_speed))
            
            # Use librosa for time stretching (speed adjustment)
            audio = librosa.effects.time_stretch(audio, rate=speech_speed)
        
        # Convert to 16-bit PCM
        audio_16bit = (audio * 32767).astype(np.int16)
        
        # Use soundfile to write to BytesIO buffer instead of wavfile
        audio_buffer = BytesIO()
        sf.write(audio_buffer, audio_16bit, sample_rate, format='WAV')
        
        # Get audio data from buffer
        audio_buffer.seek(0)
        audio_data = audio_buffer.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Close buffer
        audio_buffer.close()
        
        return audio_base64
    except Exception as e:
        print(f"Error generating speech with VITS: {e}")
        return None

# Function definitions for OpenAI function calling
function_definitions = [
    {
        "name": "get_weather",
        "description": "Get current weather information for a specific city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "country": {"type": "string", "description": "The country name (optional)"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_forecast",
        "description": "Get weather forecast for a specific city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "country": {"type": "string", "description": "The country name (optional)"},
                "days": {"type": "integer", "description": "Number of days for forecast (1-5)", "default": 5}
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_flights",
        "description": "Search for flights between two cities",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Origin city"},
                "destination": {"type": "string", "description": "Destination city"},
                "departure_date": {"type": "string", "description": "Departure date (YYYY-MM-DD)"},
                "return_date": {"type": "string", "description": "Return date (YYYY-MM-DD, optional)"}
            },
            "required": ["origin", "destination", "departure_date"]
        }
    },
    {
        "name": "search_hotels",
        "description": "Search for hotels in a specific city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "check_in": {"type": "string", "description": "Check-in date (YYYY-MM-DD)"},
                "check_out": {"type": "string", "description": "Check-out date (YYYY-MM-DD)"},
                "guests": {"type": "integer", "description": "Number of guests", "default": 2}
            },
            "required": ["city", "check_in", "check_out"]
        }
    },
    {
        "name": "get_attractions",
        "description": "Get tourist attractions in a specific city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "category": {"type": "string", "description": "Category of attractions (historical, cultural, nature, all)", "default": "all"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_travel_tips",
        "description": "Get travel tips for a specific destination",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "The destination name"}
            },
            "required": ["destination"]
        }
    }
]

# Function call handler
async def handle_function_call(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Handle function calls from OpenAI"""
    try:
        if function_name == "get_weather":
            return await get_weather(arguments["city"], arguments.get("country", ""))
        elif function_name == "get_forecast":
            return await get_forecast(arguments["city"], arguments.get("country", ""), arguments.get("days", 5))
        elif function_name == "search_flights":
            return await search_flights(
                arguments["origin"],
                arguments["destination"],
                arguments["departure_date"],
                arguments.get("return_date")
            )
        elif function_name == "search_hotels":
            return await search_hotels(
                arguments["city"],
                arguments["check_in"],
                arguments["check_out"],
                arguments.get("guests", 2)
            )
        elif function_name == "get_attractions":
            return await get_attractions(arguments["city"], arguments.get("category", "all"))
        elif function_name == "get_travel_tips":
            return await get_travel_tips(arguments["destination"])
        else:
            return {"error": f"Unknown function: {function_name}"}
    except Exception as e:
        return {"error": f"Error executing function {function_name}: {str(e)}"}

def get_system_prompt() -> str:
    """Get the system prompt for the travel assistant"""
    return f"""You are TravelBot, an expert AI travel assistant with access to real-time data and comprehensive travel knowledge. You help users plan trips, find accommodations, search flights, check weather, discover attractions, and provide personalized travel advice.

🌟 **Your Capabilities:**
- **Real-time Weather**: Get current weather and forecasts for any destination
- **Flight Search**: Find and compare flight options between cities
- **Hotel Booking**: Search and recommend accommodations with pricing
- **Attraction Discovery**: Find tourist spots, museums, parks, and activities
- **Travel Tips**: Provide expert advice on destinations, culture, and logistics
- **Personalized Recommendations**: When personalization is enabled, provide tailored suggestions based on user preferences, travel history, and special needs

📋 **Your Knowledge Base:**
You have access to a comprehensive travel knowledge base with {len(travel_knowledge)} expert tips covering:
- Destination guides and hidden gems
- Travel safety and security advice
- Cultural etiquette and local customs
- Transportation options and tips
- Budget planning and money-saving strategies
- Food and dining recommendations
- Packing and preparation guides
- Emergency and health information

💡 **How to Assist:**
1. **Listen Actively**: Understand the user's travel needs, preferences, and constraints
2. **Use Tools**: Always use available functions to get real-time, accurate information
3. **Be Comprehensive**: Don't just answer the immediate question - anticipate related needs
4. **Personalize**: When personalization is enabled, reference user's preferences and history
5. **Stay Updated**: Use current data for weather, prices, and availability
6. **Be Practical**: Provide actionable advice with specific details
7. **Audio Summaries**: Offer to provide audio summaries for key information

🎯 **Response Style:**
- Be enthusiastic and helpful
- Use emojis to make responses engaging
- Structure information clearly with headings and bullet points
- Provide specific details (prices, times, addresses when available)
- Always offer follow-up assistance

🔧 **Personalization Features:**
When personalization is enabled, you have access to the user's:
- Travel preferences (budget, accommodation type, transport, activities)
- Travel history and favorite destinations
- Dietary restrictions and food preferences
- Special needs and accessibility requirements
- Loyalty program memberships
- Emergency contacts and important information

Remember: Always use the available functions to get real-time data, leverage conversation history for personalization, and access the travel knowledge base for expert insights. When users ask about travel plans, proactively gather all relevant information they might need and offer audio summaries for key recommendations."""

async def process_chat_message(message: str, conversation_id: str, personalized: bool = False, speech_speed: float = 1.0) -> tuple[str, List[Dict], Optional[str]]:
    """Process a chat message with function calling support, memory, and TTS"""
    
    # Get or create conversation history
    if conversation_id not in conversations:
        conversations[conversation_id] = [
            {"role": "system", "content": get_system_prompt()}
        ]
    
    # Get relevant conversation history from ChromaDB
    relevant_history = get_relevant_conversation_history(message, conversation_id, limit=2)
    
    # Get relevant travel knowledge from ChromaDB
    relevant_knowledge = get_relevant_travel_knowledge(message, limit=3)
    
    # Enhance system prompt with relevant context
    enhanced_context = ""
    
    if relevant_history:
        enhanced_context += "\n\n🧠 **Relevant Conversation History:**\n"
        for hist in relevant_history:
            enhanced_context += f"- {hist['content'][:200]}...\n"
    
    if relevant_knowledge:
        enhanced_context += "\n\n📚 **Relevant Travel Knowledge:**\n"
        for knowledge in relevant_knowledge:
            enhanced_context += f"- **{knowledge['title']}**: {knowledge['content'][:150]}...\n"
    
    # Add user personalization context if enabled
    if personalized:
        enhanced_context += "\n\n👤 **User Profile & Preferences:**\n"
        enhanced_context += f"- Name: {user_mock_data['name']}\n"
        enhanced_context += f"- Preferred Budget: {user_mock_data['preferences']['budget']}\n"
        enhanced_context += f"- Preferred Accommodation: {', '.join(user_mock_data['preferences']['accommodation'])}\n"
        enhanced_context += f"- Preferred Transport: {', '.join(user_mock_data['preferences']['transport'])}\n"
        enhanced_context += f"- Food Preferences: {', '.join(user_mock_data['preferences']['food'])}\n"
        enhanced_context += f"- Preferred Activities: {', '.join(user_mock_data['preferences']['activities'])}\n"
        enhanced_context += f"- Special Needs: {user_mock_data['special_needs']}\n"
        
        # Add travel history context
        if user_mock_data['travel_history']:
            enhanced_context += f"- Recent Travel History:\n"
            for trip in user_mock_data['travel_history'][-3:]:  # Last 3 trips
                enhanced_context += f"  • {trip['destination']} ({trip['date']}) - {trip['purpose']}\n"
        
        # Add loyalty programs
        if user_mock_data['loyalty_programs']:
            loyalty_programs = [f"{prog['program']} ({prog['tier']})" for prog in user_mock_data['loyalty_programs']]
            enhanced_context += f"- Loyalty Programs: {', '.join(loyalty_programs)}\n"
    
    # Add enhanced context to the conversation if available
    if enhanced_context:
        conversations[conversation_id].append({
            "role": "system",
            "content": f"Context from your knowledge base and previous conversations:{enhanced_context}"
        })
    
    # Add user message to conversation
    conversations[conversation_id].append({
        "role": "user", 
        "content": message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Track function calls
    function_calls_made = []
    
    try:
        # Make initial API call with function calling
        response = client.chat.completions.create(
            model=model_name,
            messages=conversations[conversation_id],
            functions=function_definitions,
            function_call="auto",
            max_tokens=2000,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message
        
        # Handle function calls
        if assistant_message.function_call:
            # Add assistant message with function call
            conversations[conversation_id].append({
                "role": "assistant",
                "content": assistant_message.content,
                "function_call": {
                    "name": assistant_message.function_call.name,
                    "arguments": assistant_message.function_call.arguments
                }
            })
            
            # Execute function call
            function_name = assistant_message.function_call.name
            function_args = json.loads(assistant_message.function_call.arguments)
            
            function_result = await handle_function_call(function_name, function_args)
            function_calls_made.append({
                "function": function_name,
                "arguments": function_args,
                "result": function_result
            })
            
            # Add function result to conversation
            conversations[conversation_id].append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })
            
            # Get final response with function result
            final_response = client.chat.completions.create(
                model=model_name,
                messages=conversations[conversation_id],
                max_tokens=2000,
                temperature=0.7
            )
            
            final_message = final_response.choices[0].message.content
        else:
            final_message = assistant_message.content
        
        # Add final assistant message to conversation
        conversations[conversation_id].append({
            "role": "assistant",
            "content": final_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Store conversation in ChromaDB
        store_conversation(conversation_id, message, final_message)
        
        # Generate audio response if requested
        audio_base64 = None
        if len(final_message) > 0:
            # Try local TTS methods first (more reliable)
            audio_base64 = text_to_speech(final_message, max_length=200, speed=speech_speed)
            
            # If local TTS fails and speed control is needed, try VITS
            if not audio_base64 and speech_speed != 1.0:
                audio_base64 = generate_speech_vits(final_message, speech_speed)
            
            # OpenAI TTS is disabled due to API issues
            # if not audio_base64:
            #     audio_base64 = generate_speech_openai(final_message)
        
        # Keep conversation history manageable
        if len(conversations[conversation_id]) > 20:
            # Keep system message and last 18 messages
            conversations[conversation_id] = [conversations[conversation_id][0]] + conversations[conversation_id][-18:]
        
        return final_message, function_calls_made, audio_base64
        
    except Exception as e:
        error_message = f"I apologize, but I encountered an error while processing your request: {str(e)}"
        conversations[conversation_id].append({
            "role": "assistant",
            "content": error_message,
            "timestamp": datetime.now().isoformat()
        })
        return error_message, function_calls_made, None

# API Routes
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    conversation_id = await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            personalized = message_data.get("personalized", False)
            speech_speed = message_data.get("speech_speed", 1.0)
            
            if user_message.strip():
                # Process the message
                response, function_calls, audio_base64 = await process_chat_message(user_message, conversation_id, personalized, speech_speed)
                
                # Send response back to client
                response_data = {
                    "response": response,
                    "function_calls": function_calls,
                    "audio_base64": audio_base64,
                    "conversation_id": conversation_id
                }
                
                await manager.send_personal_message(json.dumps(response_data), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """REST API endpoint for chat"""
    try:
        conversation_id = request.conversation_id
        response, function_calls, audio_base64 = await process_chat_message(request.message, conversation_id, request.personalized, request.speech_speed)
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            function_calls=function_calls,
            audio_base64=audio_base64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id in conversations:
        return {"conversation_id": conversation_id, "messages": conversations[conversation_id]}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

@app.get("/api/conversations")
async def list_conversations():
    """List all active conversations"""
    conversation_list = []
    for conv_id, messages in conversations.items():
        # Get the first user message as preview
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        preview = user_messages[0]["content"][:100] + "..." if user_messages else "New conversation"
        
        conversation_list.append({
            "conversation_id": conv_id,
            "preview": preview,
            "message_count": len(messages),
            "last_updated": messages[-1].get("timestamp") if messages else None
        })
    
    return {"conversations": conversation_list}

@app.post("/api/tts")
async def generate_tts(request: TTSRequest):
    """Generate text-to-speech audio for given text with speed control"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Validate speed parameter
        if request.speed < 0.5 or request.speed > 2.0:
            raise HTTPException(
                status_code=400, 
                detail="Speech speed must be between 0.5 and 2.0"
            )
        
        audio_base64 = text_to_speech(
            request.text, 
            max_length=request.max_length, 
            speed=request.speed
        )
        
        if audio_base64:
            return {
                "audio_base64": audio_base64, 
                "text": request.text,
                "speed": request.speed,
                "max_length": request.max_length
            }
        else:
            raise HTTPException(status_code=500, detail="TTS generation failed")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

# Export functionality
def export_messages_to_excel(messages: List[Dict[str, Any]], filename: Optional[str] = None) -> BytesIO:
    """Export messages to Excel format"""
    if not filename:
        filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Create a workbook and worksheet
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Prepare data for Excel
        data = []
        for msg in messages:
            data.append({
                'Role': msg.get('role', 'unknown'),
                'Content': msg.get('content', ''),
                'Timestamp': msg.get('timestamp', ''),
                'Function Call': msg.get('function_call', {}).get('name', '') if msg.get('function_call') else ''
            })
        
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Chat Messages', index=False)
        
        # Get the workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Chat Messages']
        
        # Adjust column width for content
        worksheet.column_dimensions['B'].width = 100  # Content column
        
        # Style the header
        from openpyxl.styles import Font, PatternFill
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
    
    output.seek(0)
    return output

def export_messages_to_txt(messages: List[Dict[str, Any]], filename: Optional[str] = None) -> StringIO:
    """Export messages to TXT format"""
    if not filename:
        filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    output = StringIO()
    
    for i, msg in enumerate(messages):
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', '')
        
        if content.strip():  # Only add non-empty content
            if role == 'user':
                output.write(f"👤 USER: {content}\n")
            elif role == 'assistant':
                output.write(f"🤖 ASSISTANT: {content}\n")
            elif role == 'system':
                output.write(f"⚙️ SYSTEM: {content}\n")
            
            if timestamp:
                output.write(f"   📅 {timestamp}\n")
            
            # Add separator between messages (except for the last one)
            if i < len(messages) - 1:
                output.write("\n" + "="*50 + "\n\n")
    
    output.seek(0)
    return output

@app.post("/api/export")
async def export_messages(request: ExportRequest):
    """Export selected messages to Excel or TXT format"""
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided for export")
        
        if request.format.lower() not in ['excel', 'txt']:
            raise HTTPException(status_code=400, detail="Format must be 'excel' or 'txt'")
        
        # Generate filename if not provided
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if not request.filename:
            base_filename = f"chat_export_{timestamp}"
        else:
            base_filename = request.filename.replace('.xlsx', '').replace('.txt', '')
        
        if request.format.lower() == 'excel':
            filename = f"{base_filename}.xlsx"
            file_content = export_messages_to_excel(request.messages, filename)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            return StreamingResponse(
                BytesIO(file_content.getvalue()),
                media_type=media_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        
        else:  # txt format
            filename = f"{base_filename}.txt"
            file_content = export_messages_to_txt(request.messages, filename)
            media_type = "text/plain"
            
            return StreamingResponse(
                StringIO(file_content.getvalue()),
                media_type=media_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting messages: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        # Get ChromaDB statistics
        conversation_count = user_conversations_collection.count()
        knowledge_count = travel_knowledge_collection.count()
        
        return {
            "active_conversations": len(conversations),
            "stored_conversations": conversation_count,
            "knowledge_base_entries": knowledge_count,
            "tts_available": tts_model is not None,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)