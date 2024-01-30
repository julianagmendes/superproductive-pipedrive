import json
import requests
import secrets
import string
from apps.pipedrive.models import PipedriveWebhook
from apps.core.utils.authentication_tools import renew_token
from apps.core.models import PlatformIntegration

from django.db import IntegrityError

def create_pipedrive_webhook(tenant):
    # Make API request to create a webhook in Pipedrive
    with open('pipedrive_access_boacodes.json', 'r') as file:
        token_info = json.load(file)
        print(f"token info: {token_info}")

    # Use the refresh token to obtain a new access token
    access_token = token_info.get('access_token')

    # Pipedrive API endpoint for webhooks
    url = "https://api.pipedrive.com/v1/webhooks"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    tenant_password = generate_password()
    # Payload for creating the webhook
    payload = {
        "subscription_url": f"https://42c9-2603-6081-1703-485c-c86d-93b3-2750-dac9.ngrok-free.app/pipedrive/webhook/new-activity/{tenant}",
        "event_action": "added",
        "event_object": "activity",
        "http_auth_user": tenant,
        "http_auth_password": tenant_password,
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    if response.status_code == 201:
        print("Pipedrive webhook created successfully")
    elif response.status_code == 401:
        # Token expired, renew the token and retry
        renew_token()
        create_pipedrive_webhook(tenant)
    else:
        print("Failed to create Pipedrive webhook")

def generate_password():
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    return password