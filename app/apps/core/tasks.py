from celery import shared_task
from user_management.models import Company
from django.db import connection
from django_tenants.utils import get_tenant_model

# @shared_task
# def create_proposal_email_template(schema_name):
#     try:
#         tenant = get_tenant_model().objects.get(schema_name=schema_name)
#         # Set the schema explicitly within the task
#         with connection.set_tenant(tenant):
#             tenant = Company.objects.get(schema_name=schema_name)
#             print(f"Tenant5: {tenant}")

#             # Print the current schema according to the db
#             print(f"Current schema: {connection.schema_name}")

#             # Create the email template
#             email_template = EmailTemplates.objects.create(
#                 name="proposal-email-template",
#                 subject="Proposal Email",
#                 body="This is a proposal email template.",
#                 company=tenant
#             )
#             email_template.save()

#             print(f"Email template created for tenant {tenant.schema_name}")

#     except Exception as e:
#         print(f"Error creating email template: {e}")
#         raise e
