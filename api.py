import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from endee import Endee
from groq import Groq  # NEW: Using Groq instead of Gemini

# 1. Secure API Key Loading
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY environment variable is not set!")

groq_client = Groq(api_key=GROQ_API_KEY)

# 2. Initialize FastAPI & AI Infrastructure
app = FastAPI(title="Code-Lens RAG API", description="Powered by Endee Vector DB and Groq")

print("Booting Embedding Model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Connecting to Endee Database...")
endee_client = Endee()
index = endee_client.get_index(name="codebase")

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_codebase(request: QueryRequest):
    try:
        # Step 1: Embed the question
        query_vector = embedding_model.encode(request.question).tolist()
        
        # Step 2: Retrieve from Endee Vector Database
        results = index.query(vector=query_vector, top_k=3)
        
        # Step 3: Format the context
        context = ""
        for res in results:
            meta = res.get('meta', {})
            file_name = meta.get('file', 'Unknown')
            text = meta.get('text', '')
            context += f"\n--- File: {file_name} ---\nCode:\n{text}\n"

        if not context:
            return {"answer": "No relevant code found in the Endee database."}

        # Step 4: The Agentic Prompt
        prompt = f"""
        You are an elite Senior Software Engineer AI Agent. 
        Use ONLY the following codebase context retrieved from our Endee Vector Database to answer the user's question.
        If the context does not contain the answer, explicitly state: "The retrieved codebase context does not contain the answer."
        
        CONTEXT:
        {context}
        
        USER QUESTION: {request.question}
        """
        
        # Step 5: Generate answer using Groq (Llama 3)
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", 
        )
        
        return {
            "question": request.question, 
            "answer": chat_completion.choices[0].message.content, 
            "sources_used": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))