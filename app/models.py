# app/models.py
from typing import Optional
from pydantic import BaseModel, Field

class EvaluateDataRequest(BaseModel):
    latitude: float = Field(..., example=34.0522)
    longitude: float = Field(..., example=-118.2437)
    context: str = Field(..., example="I want to compare reflectance data with my ground measurements.")

class EvaluateDataResponse(BaseModel):
    user_friendly_response: str

class MetadataResponse(BaseModel):
    satellite: str
    acquisition_date: str
    acquisition_time: str
    latitude: float
    longitude: float
    wrs_path: int
    wrs_row: int
    cloud_coverage: float
    image_quality: str
