from fastapi import FastAPI, Request
from core.database import engine, Base
from auth.routes import router as user_router
from core.exceptions import global_exception_handler

app = FastAPI(
    title="Unified Data Intelligence & Forecasting Platform",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(user_router)

# Global exception handler
@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, exc: Exception):
    return global_exception_handler(request, exc)

@app.get("/")
def root():
    return {"status": "Backend running safely"}
