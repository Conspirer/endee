import os
from sentence_transformers import SentenceTransformer
from endee import Endee, Precision # Ensure this matches the actual import name for their library


# 1. Initialize the embedding model globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_code_files(repo_path, extensions=('.py', '.js', '.md')):
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                code_files.append(os.path.join(root, file))
    return code_files

def chunk_code(file_content, chunk_size=500):
    return [file_content[i:i + chunk_size] for i in range(0, len(file_content), chunk_size)]

def build_vector_database(repo_path):
    print(f"Starting ingestion for repository: {repo_path}")
    
    # 2. INITIALIZE ENDEE CLIENT (Check their docs for exact syntax!)
    client = Endee()
    
    # 3. CREATE COLLECTION WITH EXACT DIMENSIONS
    # This is where your 384 dimension size is critical.
    print("Checking database indices...")
    try:
        client.create_index(
            name="codebase",
            dimension = 384,
            space_type = "cosine",
            precision = "float32"
        )
        print("SUCCESS: Index 'codebase' created.")
    except Exception as e:
        print(f"Note during index execution: {e}")

    print("Fetching index 'codebase'...")

    index = client.get_index(name="codebase")


    files = get_code_files(repo_path)
    if not files:
        print("Error: No valid code files found.")
        return

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            chunks = chunk_code(content)
            
            for i, chunk in enumerate(chunks):
                # 4. Generate the 384-dimensional vector
                vector = model.encode(chunk).tolist()
                
                chunk_id = f"{file_path}_chunk_{i}"
                
                # 5. INSERT INTO ENDEE (Check their docs for exact syntax!)
                index.upsert([
                    {
                    "id": chunk_id, 
                    "vector": vector, 
                    "meta": {"file": file_path, "text": chunk}
                    }

                ])
                
            print(f"Successfully ingested: {file_path}")
                
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    print("Ingestion complete. Endee database populated.")

if __name__ == "__main__":
    # Point this to a small project folder on your machine first to test
    TARGET_REPO = "/home/ubermensch/Bellum/WhatBytes_Django/config/" # Example: Pointing to a parent directory or a specific project
    build_vector_database(TARGET_REPO)