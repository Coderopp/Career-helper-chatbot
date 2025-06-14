import streamlit as st
import os
from components.chat_interface import render_chat_interface # Import the function

# Main Streamlit app
st.set_page_config(layout="wide", page_title="Career Discovery Chatbot")

st.title("Career Discovery Chatbot")

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'conversation_flow' not in st.session_state:
    st.session_state.conversation_flow = 'onboarding' # Default starting flow

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
            st.info("You can manually run: python setup.py")
    else:
        st.session_state.db_initialized = True

# Render the chat interface based on the current flow state
render_chat_interface()

# TODO: Add imports for other core modules as needed (e.g., CareerCounselor)
