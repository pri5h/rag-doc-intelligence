# app/core/rag.py
import ollama
from app.core.vectorstore import search_similar_chunks

def generate_answer(query: str, top_k: int = 3):
    """
    Retrieves relevant chunks and uses a local Ollama LLM to generate a grounded answer.
    """
    # 1. Retrieve relevant chunks from our Vector DB
    results = search_similar_chunks(query, top_k=top_k)
    
    # 2. Format the chunks into a single text block for the prompt
    context = "\n\n---\n\n".join([
        f"[Source: Page {r['page_number']}]\n{r['text']}" 
        for r in results
    ])
    
    # 3. Build the strict prompt
    system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided context. 
    If the answer is not in the context, say "I don't know based on the provided documents." 
    Always cite the page number where you found the information in your answer.
    Keep your answers concise, clear, and well-formatted."""
    
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"
    
    # 4. Call the local Ollama LLM
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        options={'temperature': 0.1} # Low temperature for factual, non-hallucinated answers
    )
    
    answer = response['message']['content']
    
    # 5. Format the final response with sources
    sources = [{"page": r['page_number'], "snippet": r['text'][:100] + "..."} for r in results]
    
    return {
        "answer": answer,
        "sources": sources
    }