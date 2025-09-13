# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    user,
    chatbot,
    progress,
    quiz,
    simplify,
    stt,
    tts,
    healthcheck
)

app = FastAPI(
    title="EduBot Backend API",
    description="API backend for EduBot: AI-powered educational support for dyslexic learners.",
    version="1.0.0",
)

# Configure CORS - adjust origins as per frontend deployment domain
origins = [
    "http://localhost",
    "http://localhost:3000",
    # add frontend URLs here, e.g. "https://yourfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from routes folder
app.include_router(user.router)
app.include_router(chatbot.router)
app.include_router(progress.router)
app.include_router(quiz.router)
app.include_router(simplify.router)
app.include_router(stt.router)
app.include_router(tts.router)
app.include_router(healthcheck.router)

# Optional: startup and shutdown event handlers
@app.on_event("startup")
async def startup_event():
    # Initialize resources, connections, caches, etc.
    print("Starting EduBot backend...")

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources, close DB connections, etc.
    print("Shutting down EduBot backend...")
