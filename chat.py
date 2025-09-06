from google import genai
import eel
import os
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()

# Get API Key
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("❌ Missing API_KEY. Please set it in .env or environment variables.")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Setup Eel
eel.init('www')

@eel.expose
def chat_with_bot(user_query: str):
    """Send user query to Gemini and return response to frontend"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # or "gemini-2.5-pro"
            contents=user_query
        )

        # ✅ Correct way to extract text
        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "⚠️ No response from Gemini."

    except Exception as e:
        print("⚠️ Backend error:", e)
        return "⚠️ Sorry, something went wrong. Please try again."

# Start frontend
eel.start('index.html', size=(1000, 1000))
