import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_engine import get_ai_response

def index(request):
    """Render the main landing page of Cosmic Voyages containing the chat widget."""
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def destinations(request):
    return render(request, 'core/destinations.html')

@csrf_exempt
def api_chat(request):
    """
    API endpoint for the chat widget.
    Receives JSON with a 'message' field and returns an AI response.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Fetch AI response using our engine
            ai_reply = get_ai_response(user_message)
            
            return JsonResponse({'status': 'success', 'reply': ai_reply})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST is allowed'}, status=405)
