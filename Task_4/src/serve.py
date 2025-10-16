from fastapi import FastAPI
from pydantic import BaseModel
from .rag_bot import answer

app = FastAPI(title="RAG Bot API")

class AskRequest(BaseModel):
    query: str
    k: int = 4

class AskResponse(BaseModel):
    answer: str
    retrieved: list

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    ans, meta = answer(req.query, k=req.k)
    return AskResponse(answer=ans, retrieved=meta)
