
# Code-Lens: Agentic Enterprise Codebase Analyst

### Project Overview & Problem Statement

Engineers frequently struggle with "context drift" when onboarding to large, complex codebases. **Code-Lens** is a production-grade AI Agent designed to provide instant, scientifically grounded insights into a repository's architecture.

Going beyond static analysis, Code-Lens features a **Dynamic Ingestion Engine** that allows users to paste any public GitHub repository URL, instantly vectorize its logic, and query it in real-time. By leveraging **Retrieval-Augmented Generation (RAG)**, it allows developers to query source code in natural language and receive context-aware explanations directly from an AI Senior Developer Agent.

### System Design & Technical Approach

The system is built as a modular, multi-tenant AI microservice:

* **Dynamic GitHub Connector**: Utilizes `GitPython` to clone remote repositories on the fly, process them into temporary file systems, and prepare them for vectorization.
* **Ingestion Engine**: Recursively crawls repositories, performs logical code chunking, and generates 384-dimensional mathematical embeddings using the `all-MiniLM-L6-v2` transformer model.
* **Vector Storage Layer**: Utilizes the **Endee Vector Database** for high-performance semantic indexing, similarity search, and multi-tenant index routing.
* **RAG API (FastAPI)**: A RESTful backend that handles the query lifecycle: Vectorizing user questions, dynamically routing to the correct Endee index, retrieving relevant code metadata, and injecting it into a high-context LLM prompt.
* **Agentic Intelligence**: Employs **Llama 3.3 (via Groq)** to act as an "Architect Agent," synthesizing retrieved code snippets into actionable technical answers while strictly avoiding hallucinations.
* **Interactive UI (Streamlit)**: A zero-code frontend dashboard allowing users to input repository URLs, view indexing status, and chat with their codebase.

### How Endee is Used

Endee serves as the backbone of the system's memory and multi-tenancy:

* **Dynamic Multi-Tenancy**: Instead of a single monolithic database, the system uses Endee to dynamically create a unique `index` for every newly ingested GitHub repository, ensuring perfect context isolation.
* **Indexing**: Indices are initialized with `cosine` similarity and `float32` precision to natively match the transformer output.
* **Semantic Retrieval**: Instead of keyword matching, we use `index.query` to find code snippets that are mathematically similar to the developer's intent.
* **Metadata Management**: Endee stores the raw code chunks along with file-path metadata, allowing the Agent to cite specific files (e.g., `apps.py`, `settings.py`) in its responses.

### Setup and Execution Instructions

#### 1. Start the Endee Server (Docker)

Ensure Docker and Docker Compose are installed and running.

```bash
sudo docker-compose up -d

```

#### 2. Configure Environment

Create a virtual environment, install dependencies, and configure your API keys securely.

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac. If it fails, use: ./venv/bin/python -m pip...
pip install -r requirements.txt

```

Create a `.env` file in the root directory and add your Groq API key:

```bash
GROQ_API_KEY=gsk_your_actual_key_here

```

#### 3. Launch the Backend API (Terminal 1)

Start the FastAPI server that handles Endee routing and LLM orchestration:

```bash
uvicorn api:app --reload

```

#### 4. Launch the Interactive UI (Terminal 2)

Start the Streamlit dashboard:

```bash
streamlit run app.py

```

#### 5. Usage

1. Open the provided `localhost` URL in your browser.
2. In the sidebar, enter a GitHub Repository URL (e.g., `https://github.com/pallets/flask`) and click **Clone & Ingest**.
3. Once the Endee DB confirms ingestion, use the chat interface to ask architectural questions about the newly indexed repository!
