import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: No API key found.")
else:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        print("VALID MODELS:", models)
    except Exception as e:
        print("API ERROR:", e)
