
from apps.google_drive.models import EmailTemplate
from .api import get_deal_products, get_deal_details
from apps.core.utils.authentication_tools import get_access_tokens_db, renew_token
from django.conf import settings

def email_tamplate_handler(deal_id, new_stage_id, tenant):
    print(f"Deal ID: {deal_id}")
    if new_stage_id == 2:
        proposal_email_template = EmailTemplate.objects.get(template_name='proposal-email-template')
    elif new_stage_id == 3:
        agreement_email_template = EmailTemplate.objects.get(template_name='agreement-email-template')
    elif new_stage_id == 4:
        invoice_email_template = EmailTemplate.objects.get(template_name='invoice-email-template')
    else:
        print("No email template for this stage")
        return False
    
    access_token = get_access_tokens_db('pipedrive').get('access_token')
    deal_details = get_deal_details(access_token, deal_id)
    if deal_details.status_code == 401:
        # Renew the token and retry
        print("Renewing token")
        refresh_token = get_access_tokens_db('pipedrive').get('refresh_token')
        access_token = renew_token('pipedrive', settings.PIPEDRIVE_OAUTH_SETTINGS, refresh_token)
        deal_details = get_deal_details(access_token, deal_id)
    
    deal = deal_details.json()['data']
    recipient_name = deal['person_id']['name']
    recipient_email = next((x['value'] for x in deal['person_id']['email'] if x['primary']), None)
    deal_title = deal['title']
    deal_value = deal['value']
    products = get_deal_products(access_token)

    print(f"Recipient Name: {recipient_name}")
    print(f"Recipient Email: {recipient_email}")
    print(f"Deal Title: {deal_title}")
    print(f"Deal Value: {deal_value}")


# def get_deal_details_task(body):
#     print(f"body: {body}")
#     print(f"Current mody keys: {body['current'].keys()}")
#     recipient_name = body['current']['person_name']
#     recipient_email = body['current']['person_id']['email'][0]['value']
#     deal_title = body['current']['title']
#     deal_value = body['current']['value']
#     access_token = get_access_tokens_db('pipedrive').get('access_token')
#     products = get_deal_products(access_token)
#     if products.status_code == 401:
#         # Renew the token and retry
#         refresh_token = get_access_tokens_db('pipedrive').get('refresh_token')
#         access_token = renew_token('pipedrive', settings.PIPEDRIVE_OAUTH_SETTINGS, refresh_token)
#         products = get_deal_products(access_token)

#     print(f"Recipient Name: {recipient_name}")
#     print(f"Recipient Email: {recipient_email}")
#     print(f"Deal Title: {deal_title}")
#     print(f"Deal Value: {deal_value}")
