from django.db import models
import string
import secrets
from user_management.models import Company
from encrypted_model_fields.fields import EncryptedCharField

class PipedriveIntegration(models.Model):
    '''
        This model is updated everytime a user authenticates with our Pipedrive App
    '''
    tenant = models.OneToOneField(Company, primary_key=True, on_delete=models.CASCADE)
    is_authenticated = models.BooleanField(default=False)
    pipedrive_domain = models.CharField(max_length=255, null=True, blank=True)
    scopes = models.CharField(max_length=255, null=True, blank=True)
    encrypted_password = EncryptedCharField(max_length=255, default='')


    def save(self, *args, **kwargs):
        # Generate a random password if it's not set
        if not self.encrypted_password:
            random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            self.encrypted_password = random_password

        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant.name} - Pipedrive Integration"


class PipedriveWebhook(models.Model):
    '''
        Stores each webhook created for a tenant
    '''
    integration = models.ForeignKey(PipedriveIntegration, on_delete=models.CASCADE)
    webhook_url = models.URLField()
    webhook_id = models.CharField(max_length=255, null=True, blank=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_object = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.integration.tenant.name} - Pipedrive Webhook"
