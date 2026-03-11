from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import engine, Base
from core.dependencies import get_current_user
from core.permissions import require_role
from core.exceptions import global_exception_handler

from auth.models import User
from auth.routes import router as user_router
from datasets.routes import router as dataset_router
from analytics.routes import router as analytics_router


# Lifespan event (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (optional cleanup)


app = FastAPI(
    title="Unified Data Intelligence & Forecasting Platform",
    version="1.0.0",
    lifespan=lifespan
)


# CORS configuration
origins = [
    "http://localhost:5173",                  # local development
    "https://data-intelligence.vercel.app"    # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(user_router)
app.include_router(dataset_router)
app.include_router(analytics_router)


# Global exception handler
@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, exc: Exception):
    return global_exception_handler(request, exc)


# Root route
@app.get("/")
def root():
    return {"status": "Backend running safely"}


# Health check (useful for Render)
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Any authenticated user
@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "message": "User profile",
        "email": current_user.email,
        "role": current_user.role
    }


# Admin only
@app.get("/admin")
def admin_route(current_user: User = Depends(require_role(["admin"]))):
    return {
        "message": "Admin access granted",
        "user": current_user.email
    }


# Admin + Analyst
@app.get("/analytics-access")
def analytics_route(current_user: User = Depends(require_role(["admin", "analyst"]))):
    return {
        "message": "Analytics access granted",
        "user": current_user.email
    }


# Admin + Analyst + Viewer
@app.get("/dashboard-access")
def dashboard_route(
    current_user: User = Depends(require_role(["admin", "analyst", "viewer"]))
):
    return {
        "message": "Dashboard access granted",
        "user": current_user.email
    }