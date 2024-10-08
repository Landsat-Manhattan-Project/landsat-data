# app/main.py

from fastapi import FastAPI
from app.routes import evaluate_data, metadata
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application with metadata for documentation
app = FastAPI(
    title="NASA Landsat Data Comparator",
    description="Web application to compare ground-based observations with Landsat satellite data.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers for different endpoints with appropriate tags for documentation
app.include_router(evaluate_data.router, tags=["Evaluate Data"])
app.include_router(metadata.router, tags=["Metadata"])

@app.get("/")
def read_root():
    """
    Root endpoint welcoming users to the API.
    """
    return {"message": "Welcome to the NASA Landsat Data Comparator API"}
