import os
from google import genai

# Create Gemini client once
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_response(prompt):
    """
    Send prompt to Gemini and return the response text.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # use free-tier model
        contents=prompt
    )
    return response.text
