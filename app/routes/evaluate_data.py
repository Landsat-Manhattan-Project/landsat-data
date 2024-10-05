# app/routes/evaluate_data.py
from fastapi import APIRouter, HTTPException
from app.models import EvaluateDataRequest, EvaluateDataResponse
from app.utils.openai_client import get_openai_response
from app.routes.metadata import get_metadata  # Import the metadata function

router = APIRouter()

@router.post("/evaluate-data", response_model=EvaluateDataResponse)
def evaluate_data(request: EvaluateDataRequest):
    """
    Evaluates satellite data based on user input and returns a tailored response.

    Args:
        request (EvaluateDataRequest): The user's input containing latitude, longitude, context, and role.

    Returns:
        EvaluateDataResponse: The AI-generated, user-friendly response.

    Raises:
        HTTPException: If there is an error during processing or API calls.
    """
    try:
        # Fetch real metadata using the provided latitude and longitude
        metadata = get_metadata(latitude=request.latitude, longitude=request.longitude)
        
        # Format metadata into a structured string for the prompt
        metadata_info = (
            f"Satellite: {metadata.satellite}\n"
            f"Acquisition Date: {metadata.acquisition_date}\n"
            f"Acquisition Time: {metadata.acquisition_time}\n"
            f"Cloud Coverage: {metadata.cloud_coverage}%\n"
            f"Image Quality: {metadata.image_quality}\n"
            f"Sun Elevation: {metadata.sun_elevation}°\n"
            f"Sun Azimuth: {metadata.sun_azimuth}°\n"
            f"Ground Sampling Distance: {metadata.ground_sampling_distance} meters/pixel\n"
            f"Projection: {metadata.projection}\n"
            f"Processing Level: {metadata.processing_level}\n"
            f"Scene ID: {metadata.scene_id}\n"
            f"Orbit Number: {metadata.orbit_number}\n"
            f"Sensor Type: {metadata.sensor_type}\n"
            f"Cloud Mask: {metadata.cloud_mask}\n"
        )
        
        # Create a comprehensive prompt combining metadata, user context, and role
        prompt = (
            f"Satellite Data:\n{metadata_info}\n\n"
            f"User Context: {request.context}\n"
            f"User Role: {request.role.capitalize()}\n\n"
            f"Please provide an explanation of the satellite data that is suitable for a {request.role}."
        )
        
        # Obtain the AI-generated response from OpenAI
        ai_response = get_openai_response(prompt, role=request.role)
        
        # Return the response encapsulated in the EvaluateDataResponse model
        return EvaluateDataResponse(user_friendly_response=ai_response)
    except Exception as e:
        # Raise a 500 Internal Server Error with the exception message
        raise HTTPException(status_code=500, detail=str(e))
