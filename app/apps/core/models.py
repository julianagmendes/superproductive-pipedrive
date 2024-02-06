from django.db import models
from user_management.models import Company
from encrypted_model_fields.fields import EncryptedCharField

class PlatformIntegration(models.Model):
    platform = models.CharField(primary_key = True,max_length=255)
    is_authenticated = models.BooleanField(default=False)
    domain = models.CharField(max_length=255, null=True, blank=True)
    scopes = models.CharField(max_length=255, null=True, blank=True)
    access_token = EncryptedCharField(max_length=255, null=True, blank=True)
    refresh_token = EncryptedCharField(max_length=255, null=True, blank=True)
