import json
import requests
import string
import secrets
from django.conf import settings
from urllib.parse import urlparse
from apps.core.models import PlatformIntegration

def get_authorization_tokens(request):
    authorization_code = request.GET.get('code')
    token_url = 'https://api.pipedrive.com/oauth/token'
    client_id = settings.PIPEDRIVE_OAUTH_SETTINGS['client_id']
    client_secret = settings.PIPEDRIVE_OAUTH_SETTINGS['client_secret']
    redirect_uri = settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
    
    data = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response
    else:
        print(f"Error: {response.text}")
        return False
    

def renew_token():
    # Load token information from the JSON file
    with open('apps/core/pipedrive_access_boacodes.json', 'r') as file:
        token_info = json.load(file)

    # Use the refresh token to obtain a new access token
    refresh_token = token_info.get('refresh_token')
    client_id = settings.PIPEDRIVE_OAUTH_SETTINGS['client_id']
    client_secret = settings.PIPEDRIVE_OAUTH_SETTINGS['client_secret']
    token_url = 'https://api.pipedrive.com/oauth/token'

    token_params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=token_params)

    if response.status_code == 200:
        new_token_info = response.json()
        # Update the token information in the JSON file
        with open('apps/core/pipedrive_access_boacodes.json', 'w') as file:
            json.dump(new_token_info, file)
        print("Token renewed successfully")
    else:
        print("Failed to renew token")


