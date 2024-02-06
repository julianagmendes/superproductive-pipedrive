# celery.py
from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PipeDriveAutomation.settings')

from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp
app = TenantAwareCeleryApp()
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
