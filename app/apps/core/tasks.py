from celery import shared_task
from user_management.models import Company
from django_tenants.utils import get_tenant_model
from django.db import connection
from django.conf import settings
from urllib.parse import urlparse
from apps.core.models import PlatformIntegration
import json

@shared_task
def create_tenant(company, company_type, company_size, comm_platform, pm_platform, file_platform):
    try:
        print('Start creating tenant')

        connection.set_schema_to_public()
        
        tenant = Company.objects.create(
            schema_name=company,
            name=company,
            company_type=company_type,
            company_size=company_size,
            communication_platform=comm_platform,
            pm_platform=pm_platform,
            file_platform=file_platform
        )
        tenant.save()

        # Set the tenant as the new schema tenant
        tenant = get_tenant_model().objects.get(schema_name=company)
        print(f"tenant: {tenant}")
        connection.set_tenant(tenant)  # Set the current tenant for the database connection

        
        print('Tenant creation completed')

    except Exception as e:
        # Log the exception and traceback
        # TODO
        raise e

@shared_task
def save_authentication_info(response, tenant):
    with open('apps/core/pipedrive_access_boacodes.json', 'w') as f:
        json.dump(response.json(), f)

    parsed_url = urlparse(response.json()['api_domain'])
    subdomain = parsed_url.netloc.split('.')[0]

    if not PlatformIntegration.objects.filter(platform='pipedrive').exists():
        new_pipedrive_integration = PlatformIntegration(
                platform='pipedrive',
                is_authenticated=True,
                domain=subdomain,
                scopes=response.json()['scope']
            )
        new_pipedrive_integration.save()
        print("Saved authentication info")
    else:
        pass
        # TODO: Update the existing record