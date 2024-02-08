import requests
import json
from django.conf import settings
import secrets
import string

def create_pipedrive_webhook(access_token, tenant, url_string, event_action, event_object, tenant_password):
    # Pipedrive API endpoint for webhooks
    url = "https://api.pipedrive.com/v1/webhooks"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Payload for creating the webhook
    payload = {
        "subscription_url": f"{settings.DOMAIN}/pipedrive/webhook/{url_string}/{tenant}",
        "event_action": event_action,
        "event_object": event_object,
        "http_auth_user": tenant,
        "http_auth_password": tenant_password,
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Create webhook response: {response.json()}")
    print(f"Create webhook response status code: {response.status_code}")
    return response


def get_all_webhooks(access_token):

    # Pipedrive API endpoint for webhooks
    api_url = "https://api.pipedrive.com/v1/webhooks"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # data = { "company_id": company_id}

    # Make the API request to get all webhooks
    response = requests.get(api_url, headers=headers)
    return response


def delete_webhook(access_token, webhook_id):

    print(f"webhook_id: {webhook_id}")
    
    # Pipedrive API endpoint for webhooks
    api_url = f"https://api.pipedrive.com/v1/webhooks/{webhook_id}"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make the API request to delete the webhook
    response = requests.delete(api_url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Webhook deleted successfully.")
    else:
        print(f"Failed to delete webhook. Status code: {response.status_code}, Response: {response.text}")


def get_deal_details(access_token, deal_id):
    # Pipedrive API endpoint for webhooks
    api_url = f"https://api.pipedrive.com/v1/deals/{deal_id}"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make the API request to get all webhooks
    response = requests.get(api_url, headers=headers)
    print(f"Deal details: {response.json()}")

    return response

# get products for deal
        
def get_deal_products(access_token):
    # Pipedrive API endpoint for webhooks
    api_url = "https://api.pipedrive.com/v1/products"

    # Headers with authorization using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make the API request to get all webhooks
    response = requests.get(api_url, headers=headers)
    print(f"Products: {response.json()}")

    return response

# get the deal details








# def get_mailbox_threads(access_token):
#     # Pipedrive API endpoint for webhooks
#     api_url = "https://api.pipedrive.com/v1/mailThreads"

#     # Headers with authorization using the access token
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#     }
#     params = {
#         "folder": "drafts"
#     }

#     # Make the API request to get all webhooks
#     response = requests.get(api_url, headers=headers, params=params)
#     print(response.text)
#     print(response.json())

#     return response
