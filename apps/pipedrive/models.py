from django.db import models
from user_management.models import Company

class PipedriveIntegration(models.Model):
    tenant = models.OneToOneField(Company, primary_key=True, on_delete=models.CASCADE)
    is_authenticated = models.BooleanField(default=False)
    pipedrive_domain = models.CharField(max_length=255, null=True, blank=True)
    scopes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Pipedrive Integration"


class PipedriveWebhook(models.Model):
    integration = models.ForeignKey(PipedriveIntegration, on_delete=models.CASCADE)
    webhook_signature = models.CharField(max_length=255, null=True, blank=True)
    webhook_url = models.URLField()
    webhook_id = models.CharField(max_length=255, null=True, blank=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.integration.tenant.name} - Pipedrive Webhook"
