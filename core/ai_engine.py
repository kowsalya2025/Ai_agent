import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_ai_response(user_input: str) -> str:
    """
    Real AI Agent using the official Google Gemini REST API.
    This bypasses all pip package namespace issues by making a direct HTTP request.
    """
    if not api_key or api_key == "your_api_key_here" or api_key == "":
        return (
            "⚠️ Real AI Agent is offline: Please open the '.env' file in your "
            "project folder and correctly set the GEMINI_API_KEY."
        )
    
    # Direct secure HTTPS call to the Gemini API using gemini-flash-latest (widest availability)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    
    system_instruction = (
        "You are Vanakam Guide AI, a highly knowledgeable and friendly travel assistant "
        "for the 'Incredible India Tours' website. You help users plan luxury travel "
        "to destinations like the Taj Mahal, Kerala, Goa, and Rajasthan. "
        "Always be welcoming, polite, and answer questions about Indian culture, food, "
        "destinations, and travel safety. Keep responses concise (2-3 sentences max) "
        "and highly engaging.\n\n"
    )
    
    prompt = f"{system_instruction}User Inquiry: {user_input}\nGuide AI:"
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    data_bytes = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            # Parse the standard Gemini JSON response format
            text_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            if not text_response:
                return "Error: AI responded with an empty message."
                
            return text_response
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        return f"API Authentication Error: {error_msg}"
    except Exception as e:
        return f"Error communicating with AI server: {str(e)}"
