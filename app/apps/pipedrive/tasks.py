from celery import shared_task
from user_management.models import Company
from django.db import connection
from tenant_schemas_celery.task import TenantTask
from .utils.api import create_pipedrive_webhook
from apps.core.utils.authentication_tools import get_access_tokens_db, renew_token
from .utils.tenant_tools import save_webhook_info
import secrets
import string
from celery.exceptions import MaxRetriesExceededError
from django.conf import settings

@shared_task(base=TenantTask, bind=True)
def create_wekbhooks_task(self):
    try:
        tenant = connection.schema_name
        token_info = get_access_tokens_db('pipedrive')

        # Create New Deal Webhook
        event_action = 'added'
        event_object = 'deal'
        url_string = f"{event_action}-{event_object}"
        tenant_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        webhook_info = create_pipedrive_webhook(token_info.get('access_token'), tenant, url_string, event_action, event_object, tenant_password)
        if webhook_info.status_code == 401:
            raise Exception("Unauthorized")
        elif webhook_info.status_code == 201:
            print("Webhook created")
            save_webhook_info(webhook_info, tenant, tenant_password, url_string)

        # Create Stage Change Webhook
        event_action = 'updated'
        event_object = 'deal'
        url_string = f"{event_action}-{event_object}"
        tenant_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        webhook_info = create_pipedrive_webhook(token_info.get('access_token'), tenant, url_string, event_action, event_object, tenant_password)
        if webhook_info.status_code == 401:
            raise Exception("Unauthorized")
        elif webhook_info.status_code == 201:
            print("Webhook created")
            save_webhook_info(webhook_info, tenant, tenant_password, url_string)

    except Exception as e:
        refresh_token = token_info.get('refresh_token')
        access_token = renew_token('pipedrive',settings.PIPEDRIVE_OAUTH_SETTINGS, refresh_token)
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
                return False