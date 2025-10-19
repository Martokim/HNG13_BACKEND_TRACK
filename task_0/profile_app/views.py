# task_0/profile_app/views.py

import os
import requests
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings

# External API endpoint
CAT_FACT_API = 'https://catfact.ninja/fact'

def profile_endpoint(request):
    """
    Handles GET request for the /me endpoint.
    Fetches profile data, UTC time, and a random cat fact.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # 1. Fetch data from external API
        cat_fact_response = requests.get(CAT_FACT_API, timeout=5)
        cat_fact_response.raise_for_status() # Raise an error for bad status codes
        cat_fact_data = cat_fact_response.json()
        cat_fact = cat_fact_data.get('fact', 'Could not retrieve a cat fact.')
    
    except requests.RequestException as e:
        # 2. Handle API failure
        cat_fact = f"Error retrieving cat fact: {str(e)}"
        
    # 3. Get current UTC time (required format is usually ISO 8601)
    current_utc_time = datetime.utcnow().isoformat() + 'Z' # 'Z' denotes Zulu/UTC time
    
    # 4. Construct the final JSON response
    response_data = {
        'full_name': settings.PROFILE_NAME,
        'email': settings.PROFILE_EMAIL,
        'stack': settings.PROFILE_STACK,
        'current_utc_time': current_utc_time,
        'cat_fact': cat_fact,
        'status': 'success'
    }

    # 5. Return the JSON response
    return JsonResponse(response_data, status=200)