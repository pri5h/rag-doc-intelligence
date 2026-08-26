# app/api/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.core.extraction import extract_text_from_pdf
from app.core.chunking import chunk_text
from app.core.vectorstore import embed_and_store

router = APIRouter()
UPLOAD_DIR = "data/uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        # Run the RAG ingestion pipeline
        pages_data = extract_text_from_pdf(file_path)
        chunks = chunk_text(pages_data)
        embed_and_store(chunks)
        
        return {
            "message": f"Successfully processed {file.filename}", 
            "pages_extracted": len(pages_data),
            "chunks_created": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))