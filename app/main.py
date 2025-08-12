from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.ollama_client import get_ollama_response
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Allow mobile app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, open to all. Use specific domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Arivya backend is running 🚀"}

@app.post("/chat")
@app.post("/chat/")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    response = get_ollama_response(message)
    return {"reply": response}  # 'reply' matches Flutter code expectation

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
