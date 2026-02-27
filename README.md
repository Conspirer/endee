# Code-Lens: Agentic Enterprise Codebase Analyst

### Project Overview & Problem Statement

Engineers frequently struggle with "context drift" when onboarding to large, complex codebases. **Code-Lens** is a production-grade AI Agent designed to provide instant, scientifically grounded insights into a repository's architecture. By leveraging **Retrieval-Augmented Generation (RAG)**, it allows developers to query their own source code in natural language and receive context-aware explanations directly from an AI Senior Developer Agent.

### System Design & Technical Approach

The system is built as a modular AI microservice:

* **Ingestion Engine**: Recursively crawls repositories, performs logical code chunking, and generates 384-dimensional mathematical embeddings using the `all-MiniLM-L6-v2` transformer model.
* **Vector Storage Layer**: Utilizes the **Endee Vector Database** for high-performance semantic indexing and similarity search.
* **RAG API (FastAPI)**: A RESTful backend that handles the query lifecycle: Vectorizing user questions, retrieving relevant code metadata from Endee, and injecting it into a high-context LLM prompt.
* **Agentic Intelligence**: Employs **Llama 3.3 (via Groq)** to act as an "Architect Agent," synthesizing retrieved code snippets into actionable technical answers while strictly avoiding hallucinations by grounding responses in the retrieved context.

### How Endee is Used

Endee serves as the backbone of the system's memory:

* **Indexing**: We initialize a codebase-specific index with `cosine` similarity and `float32` precision to match transformer output.
* **Semantic Retrieval**: Instead of keyword matching, we use `index.query` to find code snippets that are mathematically similar to the developer's intent.
* **Metadata Management**: Endee stores the raw code chunks along with file-path metadata, allowing the Agent to cite specific files (e.g., `apps.py`, `settings.py`) in its responses.

### Setup and Execution Instructions

#### 1. Start the Endee Server (Docker)

Ensure Docker and Docker Compose are installed.

```bash
sudo docker-compose up -d

```

#### 2. Configure Environment

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_api_key_here"

```

#### 3. Ingest Codebase

Point the ingestion script to your project root:

```bash
# Update TARGET_REPO in ingest.py first
python ingest.py

```

#### 4. Launch the API

```bash
uvicorn api:app --reload

```

#### 5. Query the Agent

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "How is the database configured?"}'

```

---

### Final Command

