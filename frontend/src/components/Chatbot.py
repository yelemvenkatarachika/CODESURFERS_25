from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatMessage(BaseModel):
    sender: str  # "user" or "bot"
    message: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Simulated simple chatbot response logic (to be replaced with AI integration)
def generate_bot_reply(user_message: str) -> str:
    # Placeholder logic, replace with OpenAI GPT or other chatbot service calls
    lower_msg = user_message.lower()
    if "hello" in lower_msg:
        return "Hello! How can I assist you with your learning today?"
    elif "help" in lower_msg:
        return "Sure, I'm here to help! What would you like to learn about?"
    else:
        return f"You said: '{user_message}'. Let's keep going!"

@router.post("/chatbot/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message not allowed")

    reply = generate_bot_reply(user_message)
    return ChatResponse(reply=reply)
