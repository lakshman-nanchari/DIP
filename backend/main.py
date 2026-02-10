from fastapi import FastAPI 
from core.database import engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            pass 
        return {"database": "connected"}
    except Exception as e:
        return {"error" : str(e)}