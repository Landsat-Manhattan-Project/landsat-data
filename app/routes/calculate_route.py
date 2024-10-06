from fastapi import APIRouter, HTTPException
from app.models import CalculateRequest, LandsatPassResponse
from app.utils.calculate_pass import calculate_landsat_pass

router = APIRouter()

@router.post("/calculate", response_model=LandsatPassResponse)
def calculate_route(request: CalculateRequest):
    """
    Calculates the Landsat pass based on user input and returns the result.

    Args:
        request (CalculateRequest): The user's input containing the satellite data.

    Returns:
        LandsatPassResponse: The calculated Landsat pass information
    
    Raises:
        HTTPException: If there is an error during processing or API calls.
    """
    try:
        # Calculate the Landsat pass based on the provided latitude and longitude
        dates = calculate_landsat_pass(request.latitude, request.longitude)
        
        # Return the calculated pass date encapsulated in the LandsatPassResponse model
        return LandsatPassResponse(date_landsat_8=dates[0], date_landsat_9=dates[1])
    except Exception as e:
        # Raise a 500 Internal Server Error with the exception message
        raise HTTPException(status_code=500, detail=str(e))