import streamlit as st
import os
import sys

# Set environment variables for deployment compatibility
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# Handle import errors gracefully
try:
    from components.chat_interface import render_chat_interface
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("There might be a dependency issue. Please check the requirements.txt file.")
    st.stop()

# Main Streamlit app
st.set_page_config(layout="wide", page_title="Career Discovery Chatbot")

st.title("Career Discovery Chatbot")

# Check for required environment variables
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY environment variable is required")
    st.info("Please add your Groq API key to Streamlit Cloud secrets or .env file")
    st.code("""
    # Add to Streamlit Cloud Secrets:
    GROQ_API_KEY = "your_groq_api_key_here"
    
    # Or create .env file locally:
    echo 'GROQ_API_KEY=your_groq_api_key_here' > .env
    """)
    st.stop()

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'conversation_flow' not in st.session_state:
    st.session_state.conversation_flow = 'onboarding'

# Check if vector database needs initialization  
if 'db_initialized' not in st.session_state:
    if not os.path.exists('./chroma_db'):
        st.warning("🔧 First time setup: Initializing career database...")
        try:
            from data.career_embeddings import populate_career_database
            populate_career_database()
            st.success("✅ Database initialized successfully!")
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"❌ Database initialization failed: {e}")
            st.info("Database will be initialized automatically when you start chatting.")
            st.session_state.db_initialized = False
    else:
        st.session_state.db_initialized = True

# Render the chat interface based on the current flow state
try:
    render_chat_interface()
except Exception as e:
    st.error(f"Chat interface error: {e}")
    st.info("Please check your API keys and dependencies.")
