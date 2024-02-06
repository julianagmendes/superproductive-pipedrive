import requests
import json
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from apps.core.utils.authentication_tools import get_access_tokens_db, renew_token
from django_tenants.utils import get_tenant_model
from .utils.tenant_tools import save_file_info
from .utils.api import create_drive_folder, create_file_template, AuthenticationError
from PipeDriveAutomation.utils import get_secret_dict

def create_folder_view(request, tenant):
    access_token_info = get_access_tokens_db('google-drive')
    access_token = access_token_info.get('access_token')
    print(f"Access token: {access_token}")

    try:
        folder_data = create_drive_folder(access_token)
        # Check if the HTTP status code is 201 (Created)
        if folder_data.get('error') and folder_data.get('error').get('code') == 401:
            raise Exception("Unauthorized")
        elif folder_data.get('id'):
            folder_id = folder_data.get('id')
        else:
            #TODO
            print(f"Error creating folder: {folder_data}")
            JsonResponse({'success': False})
    except AuthenticationError:
        # Renew the token and retry
        print("Need new access token")
        refresh_token = get_access_tokens_db('google-drive').get('refresh_token')
        access_token = renew_token('google-drive',settings.GOOGLE_DRIVE_OAUTH_SETTINGS, refresh_token)
        print(f"New access token info: {access_token}")

        if access_token is False:
            # Handle the case where token renewal fails
            JsonResponse({'success': False})
            # return redirect('error_page')  # Replace 'error_page' with your actual error handling view
        else:
            return redirect('create_folder', tenant=tenant)

    # Redirect to the 'create_templates' view with tenant and folder_id
    return redirect('create_templates', tenant=tenant, folder_id=folder_id)

def create_templates_view(request, tenant, folder_id):
    print(f"FOLDER ID: {folder_id}")
    access_token = get_access_tokens_db('google-drive').get('access_token')
    # template_info = get_secret_dict('email_templates')
    template_info = json.loads(open('apps/google_drive/email_templates.json').read())
    print(f"Template info: {template_info}")
    try:
        for name, content in template_info.items():
            file_id = create_file_template(access_token, folder_id, name, content)
            save_file_info(file_id, name, folder_id, tenant, content)
            print(f"File ID: {file_id}")

    except AuthenticationError:
        # Renew the token and retry
        refresh_token = get_access_tokens_db('google-drive').get('refresh_token')
        access_token = renew_token('google-drive', settings.GOOGLE_DRIVE_OAUTH_SETTINGS, refresh_token)

        print(f"Renewed access token: {access_token}")
        return redirect('create_templates', tenant=tenant, folder_id=folder_id)
        
    return JsonResponse({'success': True})

