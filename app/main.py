# app/main.py
from fastapi import FastAPI
from app.routes import evaluate_data, metadata

app = FastAPI(
    title="NASA Landsat Data Comparator",
    description="Web application to compare ground-based observations with Landsat data.",
    version="1.0.0"
)

# Include the routes
app.include_router(evaluate_data.router)
app.include_router(metadata.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the NASA Landsat Data Comparator API"}
