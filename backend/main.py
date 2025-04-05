import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
import json

# Import routers
from routers import github_router, jobs_router, match_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Deep Seek Profile Skill Matcher API",
    description="API for matching GitHub profiles with job requirements",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (in production, you should specify exact origins)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(github_router.router, prefix="/api/github", tags=["GitHub"])
app.include_router(jobs_router.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(match_router.router, prefix="/api/match", tags=["Matching"])

@app.get("/")
async def root():
    return {"message": "Deep Seek Profile Skill Matcher API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_key_set": bool(os.getenv("GROQ_API_KEY"))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)