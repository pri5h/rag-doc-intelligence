# app/main.py
from fastapi import FastAPI
from app.api import upload, query

# Initialize the FastAPI app
app = FastAPI(
    title="RAG Document Intelligence API",
    description="Upload PDFs and ask questions using Retrieval-Augmented Generation."
)

# Register the routes
app.include_router(upload.router, tags=["Upload"])
app.include_router(query.router, tags=["Query"])

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Document Intelligence API! Visit /docs to test it."}