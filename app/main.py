import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import redis
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="AI Platform API")

# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    cached: bool = False

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    cache_key = f"chat:{request.message}"
    cached = redis_client.get(cache_key)
    if cached:
        return ChatResponse(response=cached, cached=True)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": "mistral", "prompt": request.message, "stream": False}
            )
            result = response.json()
            ai_response = result.get("response", "No response from model")
            redis_client.setex(cache_key, 3600, ai_response)
            return ChatResponse(response=ai_response, cached=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
