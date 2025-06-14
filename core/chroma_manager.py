# Chroma vector database configuration and initialization
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

class ChromaManager:
    def __init__(self):
        # Initialize Chroma client with persistent storage
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = "career-discovery-collection"
        
    def get_or_create_collection(self):
        """Get or create Chroma collection"""
        try:
            collection = self.client.get_collection(name=self.collection_name)
        except ValueError:
            # Collection doesn't exist, create it
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
        return collection
    
    def get_collection(self):
        """Get existing collection"""
        return self.client.get_collection(name=self.collection_name)
    
    def search_careers(self, query, top_k=5):
        """Search careers using text query"""
        try:
            collection = self.get_collection()
            results = collection.query(
                query_texts=[query],
                n_results=top_k,
                include=['metadatas', 'documents', 'distances']
            )
            return results['metadatas'][0] if results['metadatas'] else []
        except Exception as e:
            print(f"Error searching careers: {e}")
            return []

# Usage in your app
# chroma_manager = ChromaManager()
# collection = chroma_manager.get_or_create_collection()
