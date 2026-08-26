# RAG Document Intelligence Platform

A full-stack, local Retrieval-Augmented Generation (RAG) pipeline that allows users to upload PDF documents and ask natural language questions, receiving accurate, cited answers powered by a local Large Language Model (LLM).

## Problem Statement and Solution

**The Problem:** Organizations manage massive volumes of unstructured PDF documents, including manuals, contracts, and research papers. Traditional keyword-based search fails when a user's query does not exactly match the text in the document. Furthermore, pasting entire documents into a cloud-based LLM often leads to context window limitations, data privacy concerns, and model hallucinations.

**The Solution:** A local RAG pipeline. The system ingests documents by breaking them into semantic chunks, converting them into mathematical vectors, and storing them in a Vector Database. When a user submits a query, the system retrieves the most contextually relevant chunks and feeds them to a local LLM. This ensures the generated answer is strictly grounded in the provided text, completely eliminating hallucinations and maintaining data privacy.

## System Architecture

\`\`\`mermaid
graph TD
    A[PDF Document] --> B[Text Extraction via pdfplumber]
    B --> C[Chunking via LangChain]
    C --> D[Local Embeddings via Sentence-Transformers]
    D --> E[(Chroma Vector DB)]
    F[User Query via Streamlit UI] --> G[Query Embedding]
    G --> H{Similarity Search}
    E --> H
    H --> I[Top K Relevant Chunks]
    I --> J[Local LLM Generation via Ollama]
    J --> K[Grounded Answer with Citations]
\`\`\`

## Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Clean, interactive web interface for document uploads and query execution. |
| **Backend** | FastAPI + Uvicorn | High-performance, asynchronous REST API for document ingestion and querying. |
| **Text Extraction** | \`pdfplumber\` | Robust PDF text extraction, optimized for complex layouts and tables. |
| **Chunking** | \`LangChain\` | Utilizes the \`RecursiveCharacterTextSplitter\` for context-preserving text segmentation. |
| **Embeddings** | \`sentence-transformers\` | Executes the \`all-MiniLM-L6-v2\` model locally to generate semantic vectors without external API dependencies. |
| **Vector Database** | \`ChromaDB\` | Lightweight, persistent vector database for efficient similarity search. |
| **LLM** | \`Ollama\` (llama3.2) | Zero-cost, local, and private LLM inference engine. |
| **DevOps** | Docker + GitHub Actions | Containerization for consistent deployment and automated CI/CD pipelines. |

## Installation and Setup

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose
- [Ollama](https://ollama.com/) installed and running locally

### 1. Local Development Setup
\`\`\`bash
# Clone the repository
git clone https://github.com/pri5h/rag-doc-intelligence.git
cd rag-doc-intelligence

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Pull the local LLM model
ollama pull llama3.2

# Start the Backend API server
uvicorn app.main:app --reload

# Start the Frontend UI (in a separate terminal window)
streamlit run app.py
\`\`\`

### 2. Docker Deployment (Recommended)
\`\`\`bash
# Build and start the containerized application
docker compose up --build
\`\`\`
*Once running, access the interactive API documentation at \`http://127.0.0.1:8000/docs\` and the user interface at \`http://localhost:8501\`.*

## Future Enhancements
Planned architectural and feature improvements for future iterations include:
- **Reranking:** Implementing a cross-encoder reranker (e.g., Cohere or BGE-reranker) to improve the precision of the top-K retrieved chunks before LLM generation.
- **Conversational Memory:** Integrating chat history and session state to allow users to ask contextual follow-up questions.
- **Multi-Document Support:** Expanding the vector database schema to support querying across multiple documents simultaneously, with metadata filtering by date, author, or document type.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
