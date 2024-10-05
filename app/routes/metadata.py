# app/routes/metadata.py
from fastapi import APIRouter, HTTPException, Query
from app.models import MetadataResponse

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def get_metadata(
    latitude: float = Query(..., example=34.0522),
    longitude: float = Query(..., example=-118.2437)
):
    try:
        # TODO: Add logic to fetch actual metadata based on latitude and longitude
        # For simplicity, we'll use simulated data
        metadata = MetadataResponse(
            satellite="Landsat 8",
            acquisition_date="2024-04-27",
            acquisition_time="10:15:30",
            latitude=latitude,
            longitude=longitude,
            wrs_path=34,
            wrs_row=45,
            cloud_coverage=12.5,
            image_quality="Good"
        )
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
