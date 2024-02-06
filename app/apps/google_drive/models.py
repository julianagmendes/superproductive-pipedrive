
from django.db import models
from apps.core.models import PlatformIntegration
from user_management.models import Company

class EmailTemplate(models.Model):
    template_name = models.CharField(primary_key= True, max_length=255)
    file_id = models.CharField(max_length=255, null=True, blank=True)
    folder_id = models.CharField(max_length=255, null=True, blank=True)
    platform = models.ForeignKey(PlatformIntegration, on_delete=models.CASCADE, blank=False, null=False)  
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)





