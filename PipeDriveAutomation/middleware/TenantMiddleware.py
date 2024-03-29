from django.core.exceptions import DisallowedHost
from django.db import connection
from django_tenants.utils import remove_www, get_public_schema_name, get_tenant_types, \
    has_multi_type_tenants, get_tenant_domain_model, get_public_schema_urlconf

from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_tenant_model


class CustomTenantMainMiddleware(TenantMainMiddleware):
    def hostname_from_request(self, request):
        """ Extracts the relevant part of the URL from the request.
            Customize this method based on your URL structure.
        """
        print(f"hostname_from_request: {request.path}")
        return request.path.split('/')[-1]

    def get_tenant(self, domain_model, hostname):
        """ Retrieves the tenant based on the extracted tenant_id.
            Customize this method based on your multitenancy logic.
        """
        tenant_model = get_tenant_model()
        print(f"get_tenant: {tenant_model}")
        try:
            # Assuming your Tenant model has a field named 'tenant_id'
            tenant = tenant_model.objects.get(schema_name=hostname)
            print(f"get tenant: {tenant}")
            return tenant
        except tenant_model.DoesNotExist:
            print('Does not exist')
            # Handle the case where the tenant is not found
            return None

    def process_request(self, request):
        # Extract information from the URL path
        tenant_identifier = self.hostname_from_request(request)

        # Match the platform to the correct tenant (company-id) and set it.
        if tenant_identifier:
            try:
                tenant = get_tenant_model().objects.get(schema_name=tenant_identifier)
                print(f"tenant: {tenant}")
                connection.set_tenant(tenant)  # Set the current tenant for the database connection

                # If you want to store the tenant in the request for easy access in views
                request.tenant = tenant

                print(f"request.tenant: {request.tenant}")
            except get_tenant_model().DoesNotExist:
                pass