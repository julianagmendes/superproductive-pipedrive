import json
import requests
import string
import secrets
from django.conf import settings
from urllib.parse import urlparse
from apps.core.models import PlatformIntegration
from django.db import transaction
from functools import wraps
from django.http import JsonResponse

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
        print(f"Response data save auth: {response_data}")

        if response_data.get('api_domain') is None:
            subdomain = None
        else:
            parsed_url = urlparse(response_data['api_domain'])
            subdomain = parsed_url.netloc.split('.')[0]

        with transaction.atomic():
            # integration, created = PlatformIntegration.objects.get_or_create(
            #     platform=platform,
            #     defaults={
            #         'is_authenticated': True,
            #         'domain': subdomain,
            #         'scopes': response_data['scope'],
            #         'access_token': response_data['access_token'],
            #         'refresh_token': response_data.get('refresh_token', integration.refresh_token) if 'refresh_token' in response_data else integration.refresh_token
            #     }
            # )

            integration, created = PlatformIntegration.objects.get_or_create(
                platform=platform,
                defaults={
                    'is_authenticated': True,
                    'domain': subdomain,
                    'scopes': response_data['scope'],
                    'access_token': response_data['access_token'],
                }
            )

            # Check if 'refresh_token' is present in the response_data
            if 'refresh_token' in response_data:
                integration.refresh_token = response_data['refresh_token']
                integration.save()

            if created:
                print("Saved authentication info")
            else:
                print(f"Platform {platform} already exists. Updating...")
                integration.is_authenticated = True
                integration.domain = subdomain
                integration.scopes = response_data['scope']
                integration.access_token = response_data['access_token']
                if 'refresh_token' in response_data:
                    integration.refresh_token = response_data['refresh_token']
                integration.save()

            return True
    except Exception as e:
        print(f"Error saving authentication info: {e}")
        return False



def renew_token(platform, platform_settings, refresh_token):

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

    print(f"Token params: {token_params}")

    response = requests.post(token_url, data=token_params)

    if response.status_code == 200:
        # Update the token information in the JSON file
        save_authentication_info(response, platform)
        print("Token renewed successfully")
        return response.json()['access_token']
    else:
        print(f"Failed to renew token: {response.text}")
        print("Failed to renew token")
        return False


def get_access_tokens_db(platform):
    try:
        integration = PlatformIntegration.objects.get(platform=platform)
        token_info = {
            "access_token": integration.access_token, 
            "refresh_token": integration.refresh_token
            }
        return token_info
    except Exception as e:
        print(f"Error getting access token from database: {e}")
        return None

# def handle_token_and_errors(func):
#     @wraps(func)
#     def wrapper(request, tenant, *args, **kwargs):
#         platform = kwargs.get('platform')
#         print(f"Platform: {platform}")
#         token_info = get_access_tokens_db(platform)
#         print(f"Token info: {token_info}")
#         try:
#             access_token = token_info.get('access_token')

#             # Call the wrapped function with the access token and platform
#             response = func(request, tenant, access_token, *args, **kwargs)

#             return response

#         except Exception as e:  # Replace with the actual exception for token expiration
#             # Attempt to renew the token and retry the original function
#             if platform == 'pipedrive':
#                 new_access_token = renew_token(settings.PIPEDRIVE_OAUTH_SETTINGS, token_info.get('refresh_token'))
#                 return func(request, tenant, new_access_token, *args, **kwargs)
#             else:
#                 print(f"Error handling token: {e}")
#                 return JsonResponse({'success': False, 'error': str(e)}, status=500)

#     return wrapper