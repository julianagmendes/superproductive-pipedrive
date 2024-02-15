from django_tenants.utils import get_tenant_model
from django.db import connection
from user_management.models import Company

def create_tenant(company, company_type, company_size, comm_platform, pm_platform, file_platform):
    try:
        print('Start creating tenant')

        connection.set_schema_to_public()

        tenant = Company.objects.create(
            schema_name=company.lower().replace(' ', ''),
            name=company,
            company_type=company_type,
            company_size=company_size,
            communication_platform=comm_platform,
            pm_platform=pm_platform,
            file_platform=file_platform
        )

        print(f"Tenant created: {tenant}")

        print('Tenant creation completed')

    except Exception as e:
        # Log the exception and traceback
        # TODO
        raise e