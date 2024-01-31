from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.db import connection
from .utils.authentication_tools import  get_authorization_tokens
from apps.core.utils.authentication_tools import save_authentication_info
from django.views import View
from apps.core.tasks import create_tenant


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'core/signup.html', {'form': form})
    

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('name')
            company_type = form.cleaned_data.get('company_type')
            company_size = form.cleaned_data.get('company_size')
            comm_platform = form.cleaned_data.get('communication_platform')
            pm_platform = form.cleaned_data.get('pm_platform')
            file_platform = form.cleaned_data.get('file_platform')

            # Call the Celery task to create the tenant asynchronously
            create_tenant(company, company_type, company_size, comm_platform, pm_platform, file_platform)

            # Continue with your view logic, e.g., redirect the user to an intermediate page
            # return render(request, 'core/signup.html', {'company': company})
            return redirect('authenticate_platforms', tenant=company)
    
        return render(request, 'core/signup.html', {'form': form})

class AuthenticatePlatformsView(View):
    def get(self, request, tenant):
        return render(request, 'core/authenticate_platforms.html', {'tenant': tenant})

def authorize_view_pipedrive(request, tenant):
    print(f"tenant: {connection.schema_name}")
    print(settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri'])
    pipedrive = OAuth2Session(
        settings.PIPEDRIVE_OAUTH_SETTINGS['client_id'],
        redirect_uri=settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri']
    )
    authorization_url, state = pipedrive.authorization_url(
        settings.PIPEDRIVE_OAUTH_SETTINGS['authorization_url']
    )
    request.session['oauth_state'] = state
    request.session['platform'] = 'pipedrive'
    return redirect(authorization_url)

def authorize_view_calendly(request, tenant):
    print(f"tenant: {connection.schema_name}")
    print(settings.PIPEDRIVE_OAUTH_SETTINGS['redirect_uri'])
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
    state_param = request.GET.get('state')
    session_state = request.session.get('oauth_state')
    print(f"REQUEST GET: {request.session.get('platform')}")

    if state_param is None or state_param != session_state:
        return HttpResponseForbidden("Invalid 'state' parameter")
    
    if 'pipedrive' in request.session.get('platform'):
        platform = 'pipedrive'
        response = get_authorization_tokens(request, settings.PIPEDRIVE_OAUTH_SETTINGS)
        
    elif 'other_platform' in request.GET:
        platform = 'other_platform'
        # Handle other platform authentication
        # TODO
        pass
    else:
        platform = None
        return HttpResponseForbidden("Unknown platform")

    if response is False:
        return HttpResponse("Token exchange failed")

    # Process successful token exchange
    tenant = connection.schema_name  # Make sure to define 'connection' appropriately
    print(f"tenant: {tenant}")
    
    # Save authentication information
    response = save_authentication_info(response, platform)
    if response is False:
        return HttpResponse("Failed to save authentication information")
    
    else:
        return redirect('authenticate_platforms', tenant=tenant)
