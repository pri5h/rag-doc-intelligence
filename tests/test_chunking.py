# tests/test_chunking.py
from app.core.chunking import chunk_text

def test_chunking_creates_multiple_chunks():
    # Create a dummy long text
    long_text = "This is a sentence. " * 100 
    
    pages_data = [{"page_number": 1, "text": long_text}]
    
    # Run the chunking function
    chunks = chunk_text(pages_data, chunk_size=50, chunk_overlap=10)
    
    # Assert that it created more than 1 chunk
    assert len(chunks) > 1
    # Assert that every chunk has a page number
    for chunk in chunks:
        assert "page_number" in chunk
        assert "text" in chunk