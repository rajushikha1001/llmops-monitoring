from fastapi import APIRouter, HTTPException
from app.llm_client import FakeLLM
from app.db.models import query_recent

router = APIRouter()
llm = FakeLLM()

@router.post("/generate")
async def generate(prompt: str, user_id: str = "anonymous"):
    try:
        return llm.generate(prompt, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent")
async def recent(limit: int = 20):
    return query_recent(limit)
