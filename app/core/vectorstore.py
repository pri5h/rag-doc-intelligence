import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Initialize the local embedding model (downloads on first run)
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB to save to disk
CHROMA_PATH = "data/chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="document_chunks")

def embed_and_store(chunks: List[Dict[str, any]]):
    """
    Converts text chunks into vectors and stores them in ChromaDB.
    """
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [{"page_number": chunk["page_number"]} for chunk in chunks]
    
    # Generate embeddings
    embeddings = EMBEDDING_MODEL.encode(texts).tolist()
    
    # Add to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    print(f" Successfully stored {len(chunks)} chunks in Vector DB.")

def search_similar_chunks(query: str, top_k: int = 3) -> List[Dict[str, any]]:
    """
    Embeds the user's query and finds the most semantically similar chunks.
    """
    query_embedding = EMBEDDING_MODEL.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    formatted_results = []
    for i in range(len(results['ids'][0])):
        formatted_results.append({
            "chunk_id": results['ids'][0][i],
            "page_number": results['metadatas'][0][i]['page_number'],
            "text": results['documents'][0][i],
            "distance": results['distances'][0][i] 
        })
        
    return formatted_results