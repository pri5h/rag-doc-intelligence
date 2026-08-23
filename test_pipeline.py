import os
from app.core.extraction import extract_text_from_pdf
from app.core.chunking import chunk_text
from app.core.vectorstore import embed_and_store, search_similar_chunks

def run_rag_pipeline(pdf_path: str, query: str):
    print(f" Starting RAG Pipeline for: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f" Error: File not found at {pdf_path}")
        return

    print(" Extracting text from PDF...")
    pages_data = extract_text_from_pdf(pdf_path)
    print(f"   → Extracted {len(pages_data)} pages.")
    
    print(" Chunking text...")
    chunks = chunk_text(pages_data, chunk_size=500, chunk_overlap=50)
    print(f"   → Created {len(chunks)} chunks.")
    
    print("Embedding and storing in Vector DB...")
    embed_and_store(chunks)
    
    print(f"Searching for: '{query}'")
    results = search_similar_chunks(query, top_k=3)
    
    print("\n Top Relevant Chunks:")
    for i, res in enumerate(results, 1):
        print(f"\n--- Result {i} (Page {res['page_number']}, Distance: {res['distance']:.4f}) ---")
        # Print first 300 chars for brevity
        print(res['text'][:300] + "...") 

if __name__ == "__main__":
    SAMPLE_PDF = "data/uploads/sample.pdf"
    # Change this query to match something actually inside your PDF!
    TEST_QUERY = "What is the diffrence between break and continue?" 
    
    run_rag_pipeline(SAMPLE_PDF, TEST_QUERY)