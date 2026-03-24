import sys
try:
    from google import genai
    print("SUCCESS: Fully imported genai.")
except Exception as e:
    print("ERROR LOADING GENAI:", str(e))
