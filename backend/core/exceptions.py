from fastapi import Request
from fastapi.responses import JSONResponse

def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later."
        }
    )