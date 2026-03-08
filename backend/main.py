from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from core.database import engine, Base
from core.dependencies import get_current_user
from core.permissions import require_role
from core.exceptions import global_exception_handler

from auth.models import User
from auth.routes import router as user_router

from datasets.routes import router as dataset_router
from analytics.routes import router as analytics_router

app = FastAPI(
    title="Unified Data Intelligence & Forecasting Platform",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(user_router)
app.include_router(dataset_router)
app.include_router(analytics_router)