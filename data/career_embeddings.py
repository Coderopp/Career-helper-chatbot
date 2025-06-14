# Script to populate Chroma database with career data
import sys
import os
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def populate_career_database():
    """Populate the Chroma database with career information"""
    try:
        print("Initializing Career Counselor...")
        
        # Import after path setup and with error handling
        from core.chroma_manager import ChromaManager
        from data.sample_careers import career_data_sample
        from sentence_transformers import SentenceTransformer
        
        # Initialize components separately to avoid conflicts
        print("Setting up Chroma database...")
        chroma_manager = ChromaManager()
        collection = chroma_manager.get_or_create_collection()
        
        print("Loading embedding model...")
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        embedding_model = SentenceTransformer(model_name)
        
        print(f"Populating database with {len(career_data_sample)} careers...")
        
        documents = []
        metadatas = []
        ids = []
        
        for i, career in enumerate(career_data_sample):
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
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print("✅ Career database populated successfully!")
        
        # Test the search functionality
        print("\n🔍 Testing search functionality...")
        test_queries = ["creative design", "data analysis", "helping people", "technology"]
        
        for query in test_queries:
            query_embedding = embedding_model.encode([query]).tolist()[0]
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3,
                include=['metadatas', 'documents', 'distances']
            )
            
            career_results = results['metadatas'][0] if results['metadatas'] else []
            print(f"\nQuery: '{query}'")
            print(f"Found {len(career_results)} relevant careers:")
            for i, career in enumerate(career_results, 1):
                print(f"  {i}. {career.get('title', 'Unknown')} - {career.get('tagline', 'No tagline')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error during database population: {e}")
        return False

if __name__ == "__main__":
    populate_career_database()
