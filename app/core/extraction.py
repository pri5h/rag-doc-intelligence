import pdfplumber
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, any]]:
    """
    Extracts text from a PDF, returning a list of dictionaries 
    containing the page number and the text content of that page.
    """
    pages_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:  # Only add if the page actually has text
                pages_data.append({
                    "page_number": i + 1,
                    "text": text.strip()
                })
                
    return pages_data