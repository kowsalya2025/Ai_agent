import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        # Dump exactly what models are supported
        models = [m['name'] for m in data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        print("MODELS_OK:", models)
        with open("allowed_models.txt", "w") as f:
            f.write(json.dumps(models, indent=2))
except Exception as e:
    print("MODELS_ERROR:", e)
    with open("allowed_models.txt", "w") as f:
        f.write(str(e))
