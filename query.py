from sentence_transformers import SentenceTransformer
from endee import Endee

# 1. Load the exact same embedding model
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Connect to the Endee server and get our collection
print("Connecting to Endee database...")
client = Endee()
index = client.get_index(name="codebase")

def search_codebase(query_text, top_k=3):
    print(f"\n[?] Searching codebase for: '{query_text}'")
    
    # 3. Convert the human question into a 384-dimensional vector
    query_vector = model.encode(query_text).tolist()
    
    # 4. Ask Endee to find the closest matching vectors
    try:
        results = index.query(vector=query_vector, top_k=top_k)
        
        print("\n" + "="*40)
        print("🔍 TOP RESULTS FOUND")
        print("="*40)
        
        # Endee returns a list of result objects/dicts
        for i, res in enumerate(results):
            # Extract metadata (fallback to empty dict if missing)
            meta = res.get('meta', {})
            file_name = meta.get('file', 'Unknown File')
            snippet = meta.get('text', 'No text found')
            
            print(f"\n--- MATCH {i+1} ---")
            print(f"📄 File: {file_name}")
            # Print just the first 250 characters of the code snippet to keep the terminal clean
            print(f"💻 Snippet:\n{snippet[:250]}...\n")
            
    except Exception as e:
        print(f"Query failed: {e}")

if __name__ == "__main__":
    # Test question! Change this to something that actually exists in your WhatBytes_Django config files.
    test_question = "Where is the database connection or installed apps defined?"
    search_codebase(test_question)