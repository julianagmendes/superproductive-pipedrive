'''
Will be used to actually authenticate, save and proccess authentication data
'''

import json
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse
from apps.pipedrive.models import PipedriveIntegration


def get_authorization_tokens(request):
    # Extract the authorization code from the callback URL
    authorization_code = request.GET.get('code')
    
    # Define the parameters for the token request
    token_url = 'https://api.pipedrive.com/oauth/token'
    client_id = settings.PIPEDRIVE_OAUTH_SETTINGS['client_id']
    client_secret = settings.PIPEDRIVE_OAUTH_SETTINGS['client_secret']
    redirect_uri = redirect_uri = settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
    
    data = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    
    # Make a POST request to exchange the authorization code for an access token
    response = requests.post(token_url, data=data)
    print(response.text)
    
    if response.status_code == 200:
        
        # Return info saying that it was successful to proceed with proccess
        return response
    else:
        # Handle the case where the token exchange was not successful
        print(f"Error: {response.text}")
        return False
    
def save_authentication_info(response, tenant):
    # Save necessary info to model

    with open('pipedrive_access_boacodes.json', 'w') as f:
        json.dump(response.json(), f)

    # TODO

    # Extract the subdomain from the response
    parsed_url = urlparse(response.json()['api_domain'])
    subdomain = parsed_url.netloc.split('.')[0]

    PipedriveIntegration.objects.create(
            tenant=tenant,
            is_authenticated=True,
            pipedrive_domain=subdomain,
            scopes = response.json()['scope'],
        )
    print("Saved authentication info")
    