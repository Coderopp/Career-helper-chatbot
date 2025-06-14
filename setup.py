#!/usr/bin/env python3
"""
Setup script for Career Discovery Chatbot
This script initializes the Chroma vector database with career data
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    """Initialize the vector database with career data"""
    print("🚀 Setting up Career Discovery Chatbot...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Import after adding to path
        from core.career_counselor import CareerCounselor
        from data.sample_careers import career_data_sample
        
        print("✅ Initializing Career Counselor...")
        counselor = CareerCounselor()
        
        print(f"📚 Populating database with {len(career_data_sample)} careers...")
        counselor.populate_career_database(career_data_sample)
        
        print("✅ Career database populated successfully!")
        
        # Test the search functionality
        print("\n🔍 Testing search functionality...")
        test_queries = ["creative design", "data analysis", "helping people", "technology"]
        
        for query in test_queries:
            results = counselor.search_career_data(query, top_k=2)
            print(f"  Query: '{query}' -> Found {len(results)} careers")
            for career in results:
                print(f"    - {career.get('title', 'Unknown')}")
        
        print("\n🎉 Setup completed successfully!")
        print("You can now run: streamlit run app.py")
        
    except ImportError as e:
        print(f"❌ Error: Missing dependencies. Please install requirements first:")
        print(f"   pip install -r requirements.txt")
        print(f"   Error details: {e}")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
        
    return True

if __name__ == "__main__":
    setup_database()
