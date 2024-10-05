# app/routes/evaluate_data.py
from fastapi import APIRouter, HTTPException
from app.models import EvaluateDataRequest, EvaluateDataResponse
from app.utils.openai_client import get_openai_response

router = APIRouter()

@router.post("/evaluate-data", response_model=EvaluateDataResponse)
def evaluate_data(request: EvaluateDataRequest):
    try:
        # TODO: Add logic to fetch satellite data based on latitude and longitude
        # For simplicity, we'll use a placeholder string
        satellite_data = f"Satellite data for latitude {request.latitude} and longitude {request.longitude}."

        # Create the prompt by combining satellite data and user context
        prompt = (
            f"{satellite_data}\n"
            f"User context: {request.context}\n\n"
            f"Provide a comprehensible response for someone without technical knowledge about this raw data."
        )

        # Get the response from OpenAI
        ai_response = get_openai_response(prompt)

        return EvaluateDataResponse(user_friendly_response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
