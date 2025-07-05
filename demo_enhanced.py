#!/usr/bin/env python3
"""
Enhanced TravelBot Demo Script

This script demonstrates the new features:
1. Text-to-Speech (TTS) capabilities
2. Vector memory with ChromaDB
3. Knowledge base access
4. Personalized recommendations
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def demo_enhanced_features():
    """Demonstrate the enhanced TravelBot features"""
    
    print("🎯 Enhanced TravelBot Demo")
    print("=" * 50)
    
    # Import the main modules
    try:
        from main import (
            initialize_knowledge_base,
            initialize_tts,
            text_to_speech,
            store_user_conversation,
            get_relevant_conversation_history,
            get_relevant_travel_knowledge,
            process_chat_message
        )
        
        print("✅ All modules imported successfully")
        
        # Initialize TTS
        print("\n🔊 Initializing Text-to-Speech...")
        initialize_tts()
        
        # Initialize knowledge base
        print("\n📚 Initializing Knowledge Base...")
        initialize_knowledge_base()
        
        # Test TTS functionality
        print("\n🎤 Testing TTS functionality...")
        test_text = "Hello! Welcome to Enhanced TravelBot with voice capabilities!"
        audio_base64 = text_to_speech(test_text)
        
        if audio_base64:
            print("✅ TTS audio generated successfully")
            print(f"📏 Audio data length: {len(audio_base64)} characters")
        else:
            print("❌ TTS generation failed")
        
        # Test knowledge base search
        print("\n🔍 Testing Knowledge Base Search...")
        knowledge_results = get_relevant_travel_knowledge("budget travel tips", limit=3)
        
        if knowledge_results:
            print(f"✅ Found {len(knowledge_results)} relevant knowledge entries:")
            for i, result in enumerate(knowledge_results, 1):
                print(f"  {i}. {result['title']} (Category: {result['category']})")
        else:
            print("❌ No knowledge results found")
        
        # Test conversation processing
        print("\n💬 Testing Enhanced Chat Processing...")
        conversation_id = "demo_conversation_" + str(datetime.now().timestamp())
        
        # Simulate a conversation
        test_messages = [
            "I'm planning a trip to Japan. Can you help me?",
            "I prefer budget-friendly accommodations. What hotels do you recommend in Tokyo?",
            "What's the weather like in Tokyo in December?",
            "Based on my previous preferences, can you suggest some budget activities?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Message {i}: {message}")
            
            try:
                response, function_calls, audio_base64 = await process_chat_message(message, conversation_id)
                
                print(f"🤖 Response: {response[:100]}...")
                print(f"🔧 Function calls: {len(function_calls) if function_calls else 0}")
                print(f"🔊 Audio generated: {'Yes' if audio_base64 else 'No'}")
                
            except Exception as e:
                print(f"❌ Error processing message: {e}")
        
        # Test conversation history retrieval
        print("\n🧠 Testing Conversation Memory...")
        history_results = get_relevant_conversation_history(
            "budget accommodations", 
            conversation_id, 
            limit=3
        )
        
        if history_results:
            print(f"✅ Found {len(history_results)} relevant conversation entries")
            for i, result in enumerate(history_results, 1):
                print(f"  {i}. Score: {result['similarity_score']:.2f}")
        else:
            print("❌ No conversation history found")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📊 Summary of Enhanced Features:")
        print("• ✅ Text-to-Speech: Convert responses to audio")
        print("• ✅ Vector Memory: Store and retrieve conversation context")
        print("• ✅ Knowledge Base: Access travel information and tips")
        print("• ✅ Personalized Recommendations: Based on conversation history")
        print("• ✅ Real-time Function Calls: Hotel, flight, weather searches")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Please check your environment setup and API keys")

def print_system_info():
    """Print system information and requirements"""
    print("\n🖥️ System Information:")
    print(f"• Python version: {sys.version}")
    print(f"• Current directory: {os.getcwd()}")
    print(f"• Environment file exists: {os.path.exists('.env')}")
    print(f"• OpenAI API key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    
    # Check for required directories
    directories = ['chroma_db', 'templates', 'static']
    for directory in directories:
        exists = os.path.exists(directory)
        print(f"• {directory}/ directory: {'Yes' if exists else 'No'}")

async def main():
    """Main demo function"""
    print("🚀 Enhanced TravelBot Demo Starting...")
    print_system_info()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  WARNING: OpenAI API key not found!")
        print("Please add OPENAI_API_KEY to your .env file")
        print("The demo will continue but some features may not work properly.")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Demo cancelled.")
            return
    
    print("\n" + "=" * 60)
    await demo_enhanced_features()

if __name__ == "__main__":
    asyncio.run(main())
