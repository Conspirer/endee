from sentence_transformers import SentenceTransformer

print("Step 1: Downloading/Loading the embedding model... (This might take a minute the first time)")
# all-MiniLM-L6-v2 is extremely fast and generates 384-dimensional vectors.
model = SentenceTransformer('all-MiniLM-L6-v2')

# A sample chunk of code we might find in your project
sample_code = """
def authenticate_user(token):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
"""

print("Step 2: Generating vector embedding for the code chunk...")
vector = model.encode(sample_code)

print("\n--- RESULTS ---")
print(f"Success! The code was converted into a vector of length: {len(vector)}")
print(f"First 5 dimensions of the vector: {vector[:5]}")