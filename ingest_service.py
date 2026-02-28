import os
import shutil
import git
from sentence_transformers import SentenceTransformer
from endee import Endee

# Initialize models and client
model = SentenceTransformer('all-MiniLM-L6-v2')
client = Endee()

def ingest_from_github(repo_url):
    # Extract name and setup temp path
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    temp_dir = f"./temp_repos/{repo_name}"
    
    # 1. Clean up old data
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # 2. Clone the repository
    print(f"Cloning {repo_url}...")
    git.Repo.clone_from(repo_url, temp_dir)
    
    # 3. Create a unique index for this specific repo
    try:
        client.create_index(name=repo_name, dimension=384, space_type="cosine", precision="float32")
    except:
        pass # Index already exists
    
    index = client.get_index(name=repo_name)
    
    # 4. Walk through the code and ingest
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(('.py', '.js', '.md', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Simple 500-char chunking
                    chunks = [content[i:i + 500] for i in range(0, len(content), 500)]
                    for i, chunk in enumerate(chunks):
                        vector = model.encode(chunk).tolist()
                        index.upsert([{
                            "id": f"{repo_name}_{file}_{i}",
                            "vector": vector,
                            "meta": {"file": file, "text": chunk}
                        }])
                except Exception as e:
                    print(f"Skipped {file}: {e}")
                    
    return repo_name