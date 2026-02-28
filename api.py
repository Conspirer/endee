import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from endee import Endee
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found in .env or environment!")

groq_client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Code-Lens RAG API")

print("Booting Embedding Model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Connecting to Endee Database...")
endee_client = Endee()

# UPDATE 1: Add index_name to the request model
class QueryRequest(BaseModel):
    question: str
    index_name: str = "codebase"  # Defaults to codebase if not provided

@app.post("/ask")
async def ask_codebase(request: QueryRequest):
    try:
        # UPDATE 2: Dynamically fetch the correct index based on the frontend's request
        active_index = endee_client.get_index(name=request.index_name)
        
        query_vector = embedding_model.encode(request.question).tolist()
        results = active_index.query(vector=query_vector, top_k=3)

        print(f"DEBUG: Querying Index: {request.index_name}")
        print(f"DEBUG: Number of results from Endee: {len(results)}")
        
        context = ""
        for res in results:
            meta = res.get('meta', {})
            file_name = meta.get('file', 'Unknown')
            text = meta.get('text', '')
            context += f"\n--- File: {file_name} ---\nCode:\n{text}\n"

        if not context:
            return {"answer": "No relevant code found in the Endee database for this index."}

        prompt = f"""
        You are an elite Senior Software Engineer AI Agent. 
        Use ONLY the following codebase context retrieved from our Endee Vector Database to answer the user's question.
        If the context does not contain the answer, explicitly state: "The retrieved codebase context does not contain the answer."
        
        CONTEXT:
        {context}
        
        USER QUESTION: {request.question}
        """
        
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", 
        )
        
        return {
            "question": request.question, 
            "answer": chat_completion.choices[0].message.content, 
            "sources_used": len(results),
            "index_queried": request.index_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))