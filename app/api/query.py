# app/api/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.rag import generate_answer

router = APIRouter()

# Define the expected shape of the incoming JSON request
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3 # Number of chunks to retrieve

@router.post("/query")
async def query_document(request: QueryRequest):
    try:
        result = generate_answer(request.question, top_k=request.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))