# app/routes/metadata.py
from fastapi import APIRouter, HTTPException, Query
from app.models import MetadataResponse

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def get_metadata(
    latitude: float = Query(
        ..., 
        example=34.0522, 
        description="Latitude of the target location."
    ),
    longitude: float = Query(
        ..., 
        example=-118.2437, 
        description="Longitude of the target location."
    )
):
    """
    Retrieves metadata for a Landsat satellite image based on latitude and longitude.

    Args:
        latitude (float): Latitude of the target location.
        longitude (float): Longitude of the target location.

    Returns:
        MetadataResponse: The metadata associated with the satellite image.

    Raises:
        HTTPException: If there is an error fetching or processing metadata.
    """
    try:
        # TODO: Replace the following simulated data with actual API calls to retrieve real metadata
        metadata = MetadataResponse(
            satellite="Landsat 8",
            acquisition_date="2024-04-27",
            acquisition_time="10:15:30",
            latitude=latitude,
            longitude=longitude,
            wrs_path=34,
            wrs_row=45,
            cloud_coverage=12.5,
            image_quality="Good",
            sun_elevation=45.0,
            sun_azimuth=180.0,
            ground_sampling_distance=30.0,
            projection="UTM Zone 11N",
            processing_level="Level-1",
            scene_id="LC08_L1TP_034045_20200427_20200506_01_T1",
            orbit_number=12345,
            sensor_type="OLI/TIRS",
            cloud_mask="Clear"
        )
        return metadata
    except Exception as e:
        # Log the error and return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))
