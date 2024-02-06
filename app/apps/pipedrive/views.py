
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .utils.api import get_all_webhooks, delete_webhook, get_mailbox_threads
from .utils.tenant_tools import verify_webhook_credentials
from apps.core.utils.authentication_tools import get_access_tokens_db, renew_token
from django.conf import settings
from .utils.event_filter_tools import get_new_stage_id

@csrf_exempt
@require_POST   
def added_deal(request, tenant):
    try:
        #Print  headers
        print(request.headers)
        data = json.loads(request.body)
        print(data)
        print(data['meta'])
        print("Received Pipedrive Webhook Data:")

        # Get the password and username from basic auth
        credentials = request.headers.get('Authorization')
        print(f"Credentials: {credentials}")
        if not credentials:
            return HttpResponseForbidden()

        # Verify the webhook credentials
        if not verify_webhook_credentials(data['meta']['webhook_id'], tenant, credentials):
            return HttpResponseForbidden()
        

        return JsonResponse({'success': True})
    

    except Exception as e:
        print(f"Error processing Pipedrive webhook: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST   
def updated_deal(request, tenant):
    try:
        data = json.loads(request.body)
        print(data)
        print("Received Pipedrive Webhook Data:")

        # Get the password and username from basic auth
        credentials = request.headers.get('Authorization')
        print(f"Credentials: {credentials}")
        if not credentials or not verify_webhook_credentials(data['meta']['webhook_id'], tenant, credentials):
            return HttpResponseForbidden()
        
        new_stage_id = get_new_stage_id(data)
        get_mailbox_threads(get_access_tokens_db('pipedrive').get('access_token'))


        return JsonResponse({'success': True})
    

    except Exception as e:
        print(f"Error processing Pipedrive webhook: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_POST   
def new_activity(request, tenant):
    try:
        #Print  headers
        print(request.headers)
        data = json.loads(request.body)
        print(data)
        print("Received Pipedrive Webhook Data:")

        return JsonResponse({'success': True})
    

    except Exception as e:
        print(f"Error processing Pipedrive webhook: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def get_all_webhooks_view(request, tenant):
    access_token = get_access_tokens_db('pipedrive').get('access_token')
    refresh_token = get_access_tokens_db('pipedrive').get('refresh_token')
    print(access_token)
    print(refresh_token)
    try:
        response = get_all_webhooks(access_token)
        print(f"response status code: {response.status_code}")
        if response.status_code == 401:
            raise Exception("Unauthorized")
    except Exception as e:
        print('need to renew token')
        # Renew the token and retry
        new_access_token = renew_token('pipedrive', settings.PIPEDRIVE_OAUTH_SETTINGS, refresh_token)
        response = get_all_webhooks(new_access_token)

        # delete all webhooks
        webhooks = response.json().get('data')
        for webhook in webhooks:
            print(webhook.get('id'))
            # delete_webhook(new_access_token, webhook.get('id'))
    return JsonResponse({'success': True, 'webhooks': response.json()})

def delete_webhook_view(request, webhook_id, tenant):
    access_token = get_access_tokens_db('pipedrive').get('access_token')
    refresh_token = get_access_tokens_db('pipedrive').get('refresh_token')
    try:
        delete_webhook(access_token, webhook_id)
    except Exception as e:
        # Renew the token and retry
        new_access_token = renew_token(settings.PIPEDRIVE_OAUTH_SETTINGS, refresh_token)
        delete_webhook(new_access_token, webhook_id)

    return JsonResponse({'success': True, 'response': 'Done'})
    
