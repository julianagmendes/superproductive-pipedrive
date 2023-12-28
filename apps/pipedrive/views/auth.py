from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.db import connection
from apps.pipedrive.utils.authentication_tools import get_authorization_tokens, save_authentication_info
from django.core.cache import cache

def authorize_view(request, tenant):
    pipedrive = OAuth2Session(
        settings.PIPEDRIVE_OAUTH_SETTINGS['client_id'],
        redirect_uri=settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
    )
    authorization_url, state = pipedrive.authorization_url(
        settings.PIPEDRIVE_OAUTH_SETTINGS['authorization_url']
    )
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def callback_view(request):
    if request.GET.get('state') != request.session.get('oauth_state'):
        return HttpResponseForbidden("Invalid 'state' parameter")

    response = get_authorization_tokens(request)
    if response is False:
        return HttpResponse("Token exchange failed")
    else:
        tenant = connection.schema_name
        print(f"tenant: {tenant}")
        save_authentication_info(response, tenant)
        return redirect(f'oauth_success', tenant=tenant)

def oauth_success(request, tenant):
    return render(request, 'pipedrive/oauth_success.html')

def oauth_error(request, tenant):
    return render(request, 'pipedrive/oauth_error.html')



# from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
# import json
# import httpx
# from django.shortcuts import redirect, render
# from requests_oauthlib import OAuth2Session
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from apps.pipedrive.utils.authentication_tools import get_authorization_tokens, save_authentication_info
# from django.db import connection

# def authorize_view(request, tenant):
#     pipedrive = OAuth2Session(
#         settings.PIPEDRIVE_OAUTH_SETTINGS['client_id'],
#         redirect_uri=settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
#     )
#     authorization_url, state = pipedrive.authorization_url(
#         settings.PIPEDRIVE_OAUTH_SETTINGS['authorization_url']
#     )
#     request.session['oauth_state'] = state
#     return redirect(authorization_url)


# def callback_view(request):
#     if request.GET.get('state') != request.session.get('oauth_state'):
#         # Handle potential CSRF attack
#         return HttpResponseForbidden("Invalid 'state' parameter")
    
#     # Transfer all info to the utils file to process
#     response = get_authorization_tokens(request)
#     if response is False:
#         return HttpResponse("Token exchange failed")
    
#     else:
#         # Save necessary info to model
#         save_authentication_info(response, connection.get_tenant())
#         return redirect('oauth_success')

# def oauth_success(request):
#     return render(request, 'pipedrive/oauth_success.html')  # Assumes you have an HTML template for success


# def oauth_error(request):
#     return render(request, 'pipedrive/oauth_error.html')  # Assumes you have an HTML template for success
