# RAG Document Intelligence Platform

A full-stack, local Retrieval-Augmented Generation (RAG) pipeline that allows users to upload PDF documents and ask natural language questions, receiving accurate, cited answers powered by a local Large Language Model (LLM).

## Problem Statement and Solution

**The Problem:** Organizations manage massive volumes of unstructured PDF documents, including manuals, contracts, and research papers. Traditional keyword-based search fails when a user's query does not exactly match the text in the document. Furthermore, pasting entire documents into a cloud-based LLM often leads to context window limitations, data privacy concerns, and model hallucinations.

**The Solution:** A local RAG pipeline. The system ingests documents by breaking them into semantic chunks, converting them into mathematical vectors, and storing them in a Vector Database. When a user submits a query, the system retrieves the most contextually relevant chunks and feeds them to a local LLM. This ensures the generated answer is strictly grounded in the provided text, completely eliminating hallucinations and maintaining data privacy.

## System Architecture

```mermaid
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
