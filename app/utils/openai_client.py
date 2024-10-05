# app/utils/openai_client.py
import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_openai_response(prompt: str, max_tokens: int = 150) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",  # Cambiar a GPT-4
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        ai_response = response.json()["choices"][0]["message"]["content"].strip()
        logger.info("OpenAI API call successful.")
        return ai_response
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception: {req_err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
