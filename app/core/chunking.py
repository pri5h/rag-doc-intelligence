from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict

def chunk_text(pages_data: List[Dict[str, any]], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, any]]:
    """
    Splits extracted text into smaller, overlapping chunks while preserving metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""] 
    )
    
    chunks = []
    for page in pages_data:
        split_chunks = text_splitter.split_text(page["text"])
        
        for i, chunk_text in enumerate(split_chunks):
            chunks.append({
                "text": chunk_text,
                "page_number": page["page_number"],
                "chunk_id": f"page_{page['page_number']}_chunk_{i}"
            })
            
    return chunks