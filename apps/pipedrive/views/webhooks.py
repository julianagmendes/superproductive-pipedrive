
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import json
import httpx
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


'''
    Just wrote random stuff as a placeholder for now
'''

@csrf_exempt
@require_POST
def webhook(request):
    try:
        data = json.loads(request.body)
        print(data)
        print("Received Pipedrive Webhook Data:")

        return JsonResponse({'success': True})
    

    except Exception as e:
        print(f"Error processing Pipedrive webhook: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST   
def new_activity(request, tenant):
    try:
        #Print  headers
        print(request.headers)
        data = json.loads(request.body)
        print(data)
        print("Received Pipedrive Webhook Data:")

        return JsonResponse({'success': True})
    

    except Exception as e:
        print(f"Error processing Pipedrive webhook: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)