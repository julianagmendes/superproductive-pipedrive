import json
import requests
import string
import secrets
from django.conf import settings
from urllib.parse import urlparse
from apps.core.models import PlatformIntegration
from django.db import transaction

def get_authorization_tokens(request, platform_settings):
    authorization_code = request.GET.get('code')
    token_url = platform_settings['token_url']
    
    data = {
        'code': authorization_code,
        'client_id': platform_settings['client_id'],
        'client_secret': platform_settings['client_secret'],
        'redirect_uri': platform_settings['redirect_uri'],
        'grant_type': 'authorization_code',
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response
    else:
        print(f"Error: {response.text}")
        return False

def save_authentication_info(response, platform):
    try:
        # Assuming response content is JSON, extract data
        response_data = json.loads(response.content)

        parsed_url = urlparse(response_data['api_domain'])
        subdomain = parsed_url.netloc.split('.')[0]

        with transaction.atomic():
            integration, created = PlatformIntegration.objects.get_or_create(
                platform=platform,
                defaults={
                    'is_authenticated': True,
                    'domain': subdomain,
                    'scopes': response_data['scope'],
                    'access_token': response_data['access_token'],
                    'refresh_token': response_data['refresh_token'],
                }
            )

            if created:
                print("Saved authentication info")
            else:
                print(f"Platform {platform} already exists. Updating...")
                integration.is_authenticated = True
                integration.domain = subdomain
                integration.scopes = response_data['scope']
                integration.access_token = response_data['access_token']
                integration.refresh_token = response_data['refresh_token']
                integration.save()

            return True
    except Exception as e:
        print(f"Error saving authentication info: {e}")
        return False



def renew_token(platform, platform_settings):
    refresh_token = get_refresh_token_db(platform)

    # Use the refresh token to obtain a new access token
    refresh_token = refresh_token
    client_id = platform_settings['client_id']
    client_secret = platform_settings['client_secret']
    token_url = platform_settings['token_url']

    token_params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=token_params)

    if response.status_code == 200:
        # Update the token information in the JSON file
        save_authentication_info(response,'pipedrive')
        print("Token renewed successfully")
    else:
        print("Failed to renew token")


def get_access_token_db(platform):
    try:
        integration = PlatformIntegration.objects.get(platform=platform)
        return integration.access_token
    except Exception as e:
        print(f"Error getting access token from database: {e}")
        return None
    
def get_refresh_token_db(platform):
    try:
        integration = PlatformIntegration.objects.get(platform=platform)
        return integration.refresh_token
    except Exception as e:
        print(f"Error getting refresh token from database: {e}")
        return None