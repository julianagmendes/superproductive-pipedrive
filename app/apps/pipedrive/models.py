from django.db import models
from apps.core.models import PlatformIntegration
from encrypted_model_fields.fields import EncryptedCharField

class Webhook(models.Model):
    '''
        Stores each webhook created for a tenant
    '''
    name = models.CharField(primary_key = True, max_length=255)
    id = models.CharField(max_length=255)
    company_id = models.CharField(max_length=255)
    integration = models.ForeignKey(PlatformIntegration, on_delete=models.CASCADE)
    password  = EncryptedCharField(max_length=255, default='')
    url = models.URLField()
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_object = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_last_called = models.DateTimeField(null=True, blank=True)