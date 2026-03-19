"""Cliente para interactuar con la API de Gemini."""

import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def get_gemini_client():
    """Inicializa y retorna el cliente de Gemini."""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL)
