# app/models.py

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class UserRole(str, Enum):
    """
    Enumeration of possible user roles.
    """
    scientist = "scientist"
    citizen = "citizen"
    farmer = "farmer"
    college_student = "college student"
    engineer = "engineer"
    biologist = "biologist"
    geologist = "geologist"

class EvaluateDataRequest(BaseModel):
    """
    Schema for the request payload to evaluate satellite data.
    """
    latitude: float = Field(
        ..., 
        example=34.0522, 
        description="Latitude of the target location."
    )
    longitude: float = Field(
        ..., 
        example=-118.2437, 
        description="Longitude of the target location."
    )
    context: str = Field(
        ..., 
        example="I want to compare reflectance data with my ground measurements.", 
        description="User-provided context or purpose of the request."
    )
    role: UserRole = Field(
        ..., 
        example="citizen", 
        description="Role of the user, e.g., 'citizen', 'scientist', 'farmer', etc."
    )

class EvaluateDataResponse(BaseModel):
    """
    Schema for the response payload after evaluating satellite data.
    """
    user_friendly_response: str

class MetadataResponse(BaseModel):
    """
    Schema for the metadata associated with a Landsat satellite image.
    """
    satellite: str = Field(
        ..., 
        example="Landsat 8", 
        description="Name of the satellite."
    )
    acquisition_date: str = Field(
        ..., 
        example="2024-04-27", 
        description="Date of image acquisition."
    )
    acquisition_time: str = Field(
        ..., 
        example="10:15:30", 
        description="Time of image acquisition."
    )
    latitude: float = Field(
        ..., 
        example=34.0522, 
        description="Latitude of the image center."
    )
    longitude: float = Field(
        ..., 
        example=-118.2437, 
        description="Longitude of the image center."
    )
    wrs_path: Optional[int] = Field(
        None, 
        example=34, 
        description="Path number in WRS-2 (Worldwide Reference System)."
    )
    wrs_row: Optional[int] = Field(
        None, 
        example=45, 
        description="Row number in WRS-2."
    )
    cloud_coverage: Optional[float] = Field(
        None, 
        example=12.5, 
        description="Percentage of cloud coverage in the image."
    )
    image_quality: Optional[str] = Field(
        None, 
        example="Good", 
        description="Quality assessment of the image."
    )
    sun_elevation: Optional[float] = Field(
        None, 
        example=45.0, 
        description="Sun elevation angle in degrees."
    )
    sun_azimuth: Optional[float] = Field(
        None, 
        example=180.0, 
        description="Sun azimuth angle in degrees."
    )
    ground_sampling_distance: Optional[float] = Field(
        None, 
        example=30.0, 
        description="Ground sampling distance in meters per pixel."
    )
    projection: Optional[str] = Field(
        None, 
        example="UTM Zone 11N", 
        description="Map projection used for the image."
    )
    processing_level: Optional[str] = Field(
        None, 
        example="Level-1", 
        description="Processing level of the data (e.g., Level-1, Level-2)."
    )
    scene_id: Optional[str] = Field(
        None, 
        example="LC08_L1TP_034045_20200427_20200506_01_T1", 
        description="Unique identifier for the scene."
    )
    orbit_number: Optional[int] = Field(
        None, 
        example=12345, 
        description="Orbit number during image acquisition."
    )
    sensor_type: Optional[str] = Field(
        None, 
        example="OLI/TIRS", 
        description="Type of sensor used for data capture."
    )
    cloud_mask: Optional[str] = Field(
        None, 
        example="Clear", 
        description="Information about cloud presence in the image."
    )
    distance_km: Optional[float] = Field(
        None, 
        example=10.5, 
        description="Distance in kilometers to the closest available data location."
    )
