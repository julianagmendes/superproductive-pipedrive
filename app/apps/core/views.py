from django.shortcuts import render
from .forms import SignUpForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.db import connection
from .utils.authentication_tools import get_oauth_authorization_url, get_authorization_tokens, save_authentication_info
from django.views import View
from django.contrib.auth import login
from django_tenants.utils import schema_context
from user_management.models import Company
from django_tenants.utils import get_tenant_model
from apps.core.tasks import create_tenant, hello_world_task
from celery import chain


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
            chain(
                create_tenant.s(
                    company,
                    company_type,
                    company_size,
                    comm_platform,
                    pm_platform,
                    file_platform),
                hello_world_task.s()
            ).apply_async()

            # Continue with your view logic, e.g., redirect the user to an intermediate page
            # return render(request, 'core/signup.html', {'company': company})
            return redirect(f'authorize', tenant=company)

        return render(request, 'core/signup.html', {'form': form})



def authorize_view(request, tenant):
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
    print(f"state: {request.GET.get('state')}")
    print(f"session: {request.session.get('oauth_state')}")
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