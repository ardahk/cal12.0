from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agents, simulation
from config import get_settings

settings = get_settings()

app = FastAPI(
    title="LLM Trading Arena API",
    description="Multi-agent AI trading system with debate mechanism",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM Trading Arena API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "llm-trading-arena"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
