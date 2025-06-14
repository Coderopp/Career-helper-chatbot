from groq import Groq
import streamlit as st
import os
# This will be a relative import if ChromaManager is in the same directory (core)
from .chroma_manager import ChromaManager 
from .llm_manager import LLMManager

class CareerCounselor:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.chroma_manager = ChromaManager()
        self.collection = self.chroma_manager.get_or_create_collection()
        self._embedding_model = None
        
        # Initialize the new LLM manager for advanced prompts
        try:
            self.llm_manager = LLMManager()
        except Exception as e:
            st.warning(f"LLM Manager initialization failed: {e}")
            self.llm_manager = None
        
    @st.cache_resource
    def get_embedding_model(_self):
        """Lazy load the embedding model with Streamlit caching to avoid PyTorch conflicts"""
        try:
            from sentence_transformers import SentenceTransformer
            model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
            return SentenceTransformer(model_name)
        except Exception as e:
            st.error(f"Error loading embedding model: {e}")
            return None
        
    @property
    def embedding_model(self):
        """Property to get the embedding model with lazy loading"""
        if self._embedding_model is None:
            self._embedding_model = self.get_embedding_model()
        return self._embedding_model
        
    def search_career_data(self, query, top_k=5):
        """Search relevant career information from Chroma"""
        try:
            if self.embedding_model is None:
                st.error("Embedding model not available")
                return []
                
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['metadatas', 'documents', 'distances']
            )
            
            return results['metadatas'][0] if results['metadatas'] else []
        except Exception as e:
            st.error(f"Error searching career data: {e}")
            return []
    
    def generate_contextual_response(self, user_input, conversation_context, flow_stage):
        """Generate response using Groq with Chroma context"""
        try:
            # Get relevant career data from Chroma
            relevant_careers = self.search_career_data(user_input)
            
            # Prepare context for Groq
            context = f"""
            You are a career counselor chatbot. Current conversation stage: {flow_stage}
            
            Relevant career information from database:
            {relevant_careers}
            
            User conversation history:
            {conversation_context}
            
            Guidelines:
            - Provide personalized career guidance
            - Use the retrieved career data to inform your responses
            - Match the conversation flow stage requirements
            - Be encouraging and supportive
            """
            
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble generating a response right now."
    
    def populate_career_database(self, career_data_list):
        """Populate Chroma with career information"""
        try:
            if self.embedding_model is None:
                st.error("Embedding model not available for database population")
                return False
                
            documents = []
            metadatas = []
            ids = []
            
            for i, career in enumerate(career_data_list):
                # Create text to embed for career description
                skills_text = ' '.join(career.get('skills', []))
                text_to_embed = f"{career['title']} {career['description']} {skills_text} {career['industry']}"
                
                # Convert metadata to ChromaDB-compatible format (no lists)
                safe_metadata = {}
                for key, value in career.items():
                    if isinstance(value, list):
                        # Convert lists to comma-separated strings
                        safe_metadata[key] = ', '.join(str(item) for item in value)
                    elif isinstance(value, (str, int, float, bool)):
                        safe_metadata[key] = value
                    else:
                        # Convert other types to string
                        safe_metadata[key] = str(value)
                
                documents.append(text_to_embed)
                metadatas.append(safe_metadata)
                ids.append(f"career_{career.get('id', i)}")
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            st.error(f"Error populating database: {e}")
            return False
