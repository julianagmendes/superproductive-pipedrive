import json
import requests
import string
import secrets
from django.conf import settings
from urllib.parse import urlparse
from apps.core.models import PlatformIntegration

def get_oauth_authorization_url(platform):
    base_url = getattr(settings, f"{platform.upper()}_OAUTH_SETTINGS")['authorization_url']
    client_id = getattr(settings, f"{platform.upper()}_OAUTH_SETTINGS")['client_id']
    redirect_uri = getattr(settings, f"{platform.upper()}_OAUTH_SETTINGS")['redirect_uri']

    oauth_authorization_url = f"{base_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    print(f"oauth_authorization_url: {oauth_authorization_url}")
    return oauth_authorization_url









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
    
def save_authentication_info(response, tenant):
    with open('pipedrive_access_boacodes.json', 'w') as f:
        json.dump(response.json(), f)

    parsed_url = urlparse(response.json()['api_domain'])
    subdomain = parsed_url.netloc.split('.')[0]

    if not PlatformIntegration.objects.filter(platform='pipedrive').exists():
        
        encrypted_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        new_pipedrive_integration = PlatformIntegration(
                platform='pipedrive',
                is_authenticated=True,
                domain=subdomain,
                scopes=response.json()['scope'],
                encrypted_password = encrypted_password
            )
        new_pipedrive_integration.save()
        print("Saved authentication info")




# '''
# Will be used to actually authenticate, save and proccess authentication data
# '''

# import json
# import requests
# from django.conf import settings
# from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from requests_oauthlib import OAuth2Session
# from urllib.parse import urlparse
# from apps.pipedrive.models import PipedriveIntegration


# def get_authorization_tokens(request):
#     # Extract the authorization code from the callback URL
#     authorization_code = request.GET.get('code')
    
#     # Define the parameters for the token request
#     token_url = 'https://api.pipedrive.com/oauth/token'
#     client_id = settings.PIPEDRIVE_OAUTH_SETTINGS['client_id']
#     client_secret = settings.PIPEDRIVE_OAUTH_SETTINGS['client_secret']
#     redirect_uri = redirect_uri = settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
    
#     data = {
#         'code': authorization_code,
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'redirect_uri': redirect_uri,
#         'grant_type': 'authorization_code',
#     }
    
#     # Make a POST request to exchange the authorization code for an access token
#     response = requests.post(token_url, data=data)
#     print(response.text)
    
#     if response.status_code == 200:
        
#         # Return info saying that it was successful to proceed with proccess
#         return response
#     else:
#         # Handle the case where the token exchange was not successful
#         print(f"Error: {response.text}")
#         return False
    
# def save_authentication_info(response, tenant):
#     # Save necessary info to model

#     with open('pipedrive_access_boacodes.json', 'w') as f:
#         json.dump(response.json(), f)

#     # TODO

#     # Extract the subdomain from the response
#     parsed_url = urlparse(response.json()['api_domain'])
#     subdomain = parsed_url.netloc.split('.')[0]

#     # Save if that tenant doesn't already exist
#     if not PipedriveIntegration.objects.filter(tenant=tenant).exists():

#         new_pipedrive_integration = PipedriveIntegration(
#                 tenant=tenant,
#                 is_authenticated=True,
#                 pipedrive_domain=subdomain,
#                 scopes = response.json()['scope'],
#             )
#         new_pipedrive_integration.save()
#         print("Saved authentication info")
        