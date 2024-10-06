# app/utils/openai_client.py

import os
import requests
from dotenv import load_dotenv
import logging
from fastapi import HTTPException

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

def get_openai_response(prompt: str, role: str, max_tokens: int = 650) -> str:
    """
    Sends a prompt to OpenAI's API and retrieves the generated response.

    Args:
        prompt (str): The prompt to send to OpenAI.
        role (str): The role of the user to tailor the response.
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
    
    # Define system messages based on user roles to guide the AI's responses
    role_system_messages = {
        "scientist": "You are a knowledgeable and precise assistant specialized in satellite data and Earth sciences.",
        "citizen": "You are a friendly and clear assistant who explains technical information in an easy-to-understand manner.",
        "farmer": "You are an assistant with expertise in agriculture and satellite data applications in farming.",
        "college student": "You are a helpful assistant who explains complex concepts in a manner suitable for college students.",
        "engineer": "You are a detailed and technical assistant with expertise in engineering applications of satellite data.",
        "biologist": "You are an expert assistant specialized in biological applications and environmental monitoring using satellite data.",
        "geologist": "You are a knowledgeable assistant focused on geological applications and earth surface monitoring using satellite data."
    }
    
    # Fallback system message if role is not recognized
    system_message = role_system_messages.get(role.lower(), "You are a helpful assistant.")

    # Construct the payload for OpenAI API
    data = {
        "model": "gpt-4o-mini",  
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7  # Controls the randomness of the output
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
