from django.db import IntegrityError
from apps.core.models import PlatformIntegration
from apps.pipedrive.models import Webhook
import base64


def save_webhook_info(response, tenant, tenant_password, url_string):
    try:
        # Save the webhook information in the database
        webhook_info = response.json().get('data', {})
        platform = PlatformIntegration.objects.get(platform='pipedrive')

        webhook, created = Webhook.objects.get_or_create(
            integration=platform,
            id=webhook_info.get('id', ''),
            defaults={
                'name': url_string,
                'company_id': webhook_info.get('company_id', ''),
                'url': webhook_info.get('subscription_url', ''),
                'password': tenant_password,
                'event_type': webhook_info.get('event_action', ''),
                'event_object': webhook_info.get('event_object', ''),
            }
        )

        if not created:
            # Handle the case where the webhook already exists
            # You may want to update the existing webhook here
            print(f"Webhook with ID {webhook_info.get('id', '')} already exists")

    except IntegrityError as e:
        # Handle integrity error, which might occur if there's a duplicate entry
        print(f"Error saving webhook information: {e}")
        # TODO: Handle the IntegrityError appropriately

    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        # TODO: Handle other exceptions appropriately

# def get_company_id(tenant):
#     try:
#         # Get the company ID for the tenant
#         company = Company.objects.get(schema_name=tenant)
#         return company.id
#     except
        

def verify_webhook_credentials(id, tenant, credentials):
    print(f"Verifying webhook credentials: {id}, {tenant}, {credentials}")

    # Decode basic credentials
    credentials = credentials.split(' ')[1]
    credentials = base64.b64decode(credentials).decode('utf-8')
    username, password = credentials.split(':')
    print(f"Username: {username}, Password: {password}")
    try:
        # Verify the webhook credentials
        webhook = Webhook.objects.get(id=id)
        if webhook.password == password and username == tenant:
            print("Webhook credentials verified")
            return True
        else:
            return False
    except Webhook.DoesNotExist:
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False