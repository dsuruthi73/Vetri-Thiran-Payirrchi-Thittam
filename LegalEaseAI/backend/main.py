
from fastapi import FastAPI
from backend.routes import router

app = FastAPI(
    title="LegalEaseAI",
    description="AI Legal Document Generator",
    version="1.0.0"
)

app.include_router(router)

@app.get("/status")
def status():
    return {
        "status": "LegalEaseAI is running"
    }