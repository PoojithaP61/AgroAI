"""
AgroAI - Plant Disease Detection System
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database import init_db
from backend.ml_service import ml_service
from backend.routers import auth, diagnosis, admin
from backend.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: startup and shutdown"""
    # Startup
    setup_logging()
    print("🚀 Starting AgroAI Backend...")
    
    # Initialize database
    print("📦 Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    # Initialize ML models
    print("🤖 Initializing ML models...")
    try:
        ml_service.initialize()
        print("✅ ML models loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: ML models failed to initialize: {e}")
        print("⚠️ Some endpoints may not work until models are available")
    
    yield
    
    # Shutdown
    print("👋 Shutting down AgroAI Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered plant disease detection and advisory system",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(diagnosis.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AgroAI - Plant Disease Detection System",
        "version": settings.VERSION,
        "docs": "/docs",
        "api_prefix": settings.API_V1_PREFIX
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    ml_status = "ready" if ml_service.classifier is not None else "not_initialized"
    
    return {
        "status": "healthy",
        "ml_models": ml_status,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
