from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.db import connection
from .utils.authentication_tools import  get_authorization_tokens, save_authentication_info
from .utils.tenant_tools import create_tenant
from django.views import View
from celery import chain
from celery.result import AsyncResult
from user_management.models import Company
from apps.google_drive.tasks import create_templates_folder_task, create_email_templates
from apps.pipedrive.tasks import create_wekbhooks_task

class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        # Get the company name from the Company model
        tenant = Company.objects.get(schema_name=connection.schema_name).name
        print(f"tenant5: {tenant}")
        return render(request, 'core/signup.html', {'form': form, 'tenant': tenant})
    

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
        tenant = Company.objects.get(schema_name=connection.schema_name).name
        return render(request, 'core/authenticate_platforms.html', {'tenant': tenant})

def authorize_view_pipedrive(request, tenant):
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

def authorize_view_google_drive(request, tenant):
    print(f"tenant: {connection.schema_name}")
    print(settings.GOOGLE_DRIVE_OAUTH_SETTINGS['redirect_uri'])
    scopes = ['https://www.googleapis.com/auth/drive.file']
    pipedrive = OAuth2Session(
        settings.GOOGLE_DRIVE_OAUTH_SETTINGS['client_id'],
        redirect_uri=settings.GOOGLE_DRIVE_OAUTH_SETTINGS['redirect_uri'],
        scope=scopes
    )
    authorization_url, state = pipedrive.authorization_url(
        settings.GOOGLE_DRIVE_OAUTH_SETTINGS['authorization_url']
    )
    request.session['oauth_state'] = state
    request.session['platform'] = 'google-drive'

    return redirect(authorization_url)


def callback_view(request):
    state_param = request.GET.get('state')
    session_state = request.session.get('oauth_state')

    print(f"REQUEST all: {request.GET}")

    # Print what the schema is
    print(f"databse schema:{connection.schema_name}")

    print(f"REQUEST GET: {request.session.get('platform')}")

    if state_param is None or state_param != session_state:
        return HttpResponseForbidden("Invalid 'state' parameter")
    
    if 'pipedrive' in request.session.get('platform'):
        platform = 'pipedrive'
        response = get_authorization_tokens(request, settings.PIPEDRIVE_OAUTH_SETTINGS)
        
    elif 'google-drive' in request.session.get('platform'):
        platform = 'google-drive'
        response = get_authorization_tokens(request, settings.GOOGLE_DRIVE_OAUTH_SETTINGS)

    else:
        platform = None
        return HttpResponseForbidden("Unknown platform")

    if response is False:
        return HttpResponse("Token exchange failed")

    # Process successful token exchange
    tenant = connection.schema_name  # Make sure to define 'connection' appropriately
    print(f"tenant db schema: {tenant}")

    # Save authentication information
    response = save_authentication_info(response, platform)
    if response is False:
        return HttpResponse("Failed to save authentication information")
    
    else:
        if platform == 'google-drive':
            workflow = chain(create_templates_folder_task.s(), create_email_templates.s())

            # Run the workflow asynchronously, passing folder_id to create_email_templates
            result = workflow.apply_async()

        elif platform == 'pipedrive':
            create_wekbhooks_task.delay()

        return redirect('authenticate_platforms', tenant=tenant)


# def index(request, tenant):
#     template_names = ['proposal-template', 'agreement-template','invoice-template']
#     button_data_objects = EmailTemplates.objects.filter(name__in=template_names)
#     [print(x.name) for x in button_data_objects]
#     print(f"button_data_objects: {button_data_objects}")

#     return render(request, 'core/email_templates.html', {'button_data_objects': button_data_objects, 'tenant': tenant})

# def get_data(request, button_name, tenant):
#     template = get_object_or_404(EmailTemplates, name=button_name)
#     print(f"template: {template}")
#     form = EmailTemplateForm(instance=template)
    
#     return render(request, 'core/get_data.html', {'form': form})

# def update_data(request, button_name, tenant):
#     if request.method == 'POST':
#         try:
#             email_template = EmailTemplates.objects.get(name=button_name)
#             email_template.body = request.POST.get('body', '')
#             email_template.save()
#             return JsonResponse({"success": True})
#         except EmailTemplates.DoesNotExist:
#             return JsonResponse({"error": f"Template with name {button_name} does not exist"})
#     else:
#         return JsonResponse({"error": "Invalid request method"})
