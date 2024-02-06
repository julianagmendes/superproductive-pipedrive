from celery import shared_task
from django.db import connection
from PipeDriveAutomation.celery import app
from tenant_schemas_celery.task import TenantTask
from apps.core.utils.authentication_tools import get_access_tokens_db, renew_token
import requests
from django.conf import settings
import json
from celery.exceptions import MaxRetriesExceededError
from .utils.api import create_drive_folder, create_file_template, AuthenticationError
from .utils.tenant_tools import save_file_info


@shared_task(base=TenantTask, bind=True)
def create_templates_folder_task(self):
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
            return folder_id
        else:
            #TODO
            print(f"Error creating folder: {folder_data}")
            return False
    except Exception as e:
        # Renew the token and retry
        print("Need new access token")
        refresh_token = get_access_tokens_db('google-drive').get('refresh_token')
        access_token = renew_token('google-drive',settings.GOOGLE_DRIVE_OAUTH_SETTINGS, refresh_token)
        print(f"New access token info: {access_token}")

        if access_token is False:
            # Handle the case where token renewal fails
            return False
            # return redirect('error_page')  # Replace 'error_page' with your actual error handling view
        else:
            try:
                print("Retrying")
                raise self.retry(exc=None, countdown=2 ** self.request.retries)
            except MaxRetriesExceededError:
                print("Max retries exceeded. Task failed after renewing access token.")



@shared_task(base=TenantTask, bind=True)
def create_email_templates(self, folder_id):
    token_info = get_access_tokens_db('google-drive')

    template_info = json.loads(open('apps/google_drive/email_templates.json').read())
    print(f"Template info: {template_info}")
    for name, content in template_info.items():
        try:
            for name, content in template_info.items():
                file_id = create_file_template(token_info['access_token'], folder_id, name, content)
                save_file_info(file_id, name, folder_id, content)
                print(f"File ID: {file_id}")

        except AuthenticationError:
            print("Authentication error")
            # Renew the token and retry
            refresh_token = token_info.get('refresh_token')
            access_token = renew_token('google-drive', settings.GOOGLE_DRIVE_OAUTH_SETTINGS, refresh_token)

            if access_token is False:
            # Handle the case where token renewal fails
                return False
                # return redirect('error_page')  # Replace 'error_page' with your actual error handling view
            else:
                try:
                    print("Retrying")
                    raise self.retry(exc=None, countdown=2 ** self.request.retries)
                except MaxRetriesExceededError:
                    print("Max retries exceeded. Task failed after renewing access token.")
