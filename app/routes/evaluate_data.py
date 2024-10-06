# app/routes/evaluate_data.py

from fastapi import APIRouter, HTTPException
from app.models import EvaluateDataRequest, EvaluateDataResponse
from app.routes.metadata import get_metadata  # Import the get_metadata function
from app.utils.openai_client import get_openai_response

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
            f"WRS Path: {metadata.wrs_path}\n"
            f"WRS Row: {metadata.wrs_row}\n"
            f"Sensor Type: {metadata.sensor_type}\n"
            f"Distance to Location: {metadata.distance_km:.2f} km\n"
        )
        
        # Create a comprehensive prompt combining metadata, user context, and role
        prompt = (
            f"Satellite Data:\n{metadata_info}\n\n"
            f"User Context: {request.context}\n"
            f"User Role: {request.role.value.capitalize()}\n\n"
            f"Please provide an explanation of the satellite data that is suitable for a {request.role.value}."
        )
        
        # Obtain the AI-generated response from OpenAI
        ai_response = get_openai_response(prompt, role=request.role.value)
        
        # Return the response encapsulated in the EvaluateDataResponse model
        return EvaluateDataResponse(user_friendly_response=ai_response)
    except HTTPException as http_exc:
        if http_exc.status_code == 404:
            return EvaluateDataResponse(
                user_friendly_response="No satellite data is available near your location to perform the evaluation."
            )
        else:
            raise http_exc
    except Exception as e:
        # Raise a 500 Internal Server Error with the exception message
        raise HTTPException(status_code=500, detail=str(e))
