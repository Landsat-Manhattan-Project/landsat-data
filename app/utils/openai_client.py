# app/utils/openai_client.py

import os
import requests
from dotenv import load_dotenv
import logging
from fastapi import HTTPException
from typing import List, Dict

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Configure logging to capture information and error messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify that the API key is set
if OPENAI_API_KEY:
    logger.info("OpenAI API key loaded successfully.")
else:
    logger.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    raise ValueError("OpenAI API key is not set.")

def get_openai_response(messages: List[Dict[str, str]], max_tokens: int = 650) -> str:
    """
    Sends a list of messages to OpenAI's API and retrieves the generated response.

    Args:
        messages (List[Dict[str, str]]): The conversation messages to send to OpenAI.
        max_tokens (int): The maximum number of tokens in the response.

    Returns:
        str: The AI-generated response.

    Raises:
        HTTPException: If the API request fails.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",  
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.8,  # Controls the randomness of the output
    }
    
    try:
        # Send the POST request to OpenAI API
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Extract the generated content from the response
        ai_response = response.json()["choices"][0]["message"]["content"].strip()
        logger.info("OpenAI API call successful.")
        return ai_response
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        # Log the response content for debugging
        logger.error(f"Response content: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=f"OpenAI API error: {response.text}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception: {req_err}")
        raise HTTPException(status_code=500, detail=f"Request exception: {req_err}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
