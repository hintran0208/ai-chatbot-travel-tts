#!/bin/bash

echo "🚀 Setting up Enhanced TravelBot with TTS and Vector Memory..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p chroma_db
mkdir -p static
mkdir -p templates

# Check if environment variables are set
echo "🔍 Checking environment variables..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set. Please add it to your .env file."
fi

echo "✅ Setup complete!"
echo ""
echo "🎉 Enhanced TravelBot Features:"
echo "🔊 Text-to-Speech: AI responses can be spoken aloud"
echo "🧠 Vector Memory: Chatbot remembers past conversations and preferences"
echo "📚 Knowledge Base: Access to extensive travel information"
echo "🎯 Personalized Recommendations: Based on conversation history"
echo "🚀 Real-time Function Calls: Hotel, flight, weather, and activity searches"
echo ""
echo "🌟 New API Endpoints:"
echo "• GET /api/stats - System statistics and capabilities"
echo "• POST /api/tts - Generate text-to-speech audio"
echo "• GET /api/knowledge/search - Search travel knowledge base"
echo "• GET /api/conversation/{id}/knowledge - Get conversation context"
echo ""
echo "To start the server:"
echo "source venv/bin/activate"
echo "python main.py"
echo ""
echo "Or use the provided script:"
echo "./start.sh"
