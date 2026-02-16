import os
from google import genai
from pypdf import PdfReader

_client = None


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file object.
    
    Args:
        pdf_file: A file-like object containing PDF data
        
    Returns:
        str: Extracted text from all pages in the PDF
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}") from e


def get_client():
    """Lazily initialize and return a Gemini `genai.Client`.

    Raises a RuntimeError with a clear message if the environment
    is not configured or client initialization fails.
    """
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Set it before calling Gemini functions."
        )

    try:
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini client: {e}") from e


def get_response(prompt, model="gemini-2.5-flash"):
    """Send `prompt` to Gemini and return the response text.

    This function wraps client creation and surfaces helpful errors
    rather than raising library-internal exceptions at import time.
    """
    try:
        client = get_client()
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text
    except Exception as e:
        # Surface a friendly error that callers (e.g., the UI) can display.
        raise RuntimeError(f"Error generating response from Gemini: {e}") from e

