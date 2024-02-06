import json
from datetime import datetime
from apps.core.models import PlatformIntegration
from apps.google_drive.models import EmailTemplate
from user_management.models import Company
from django.db import connection

def save_file_info(file_id, file_name, folder_id, content):
    try:
        # Save the file information in the database
        platform = PlatformIntegration.objects.get(platform='google-drive')
        tenant = connection.schema_name
        company = Company.objects.get(schema_name=tenant)
        file = EmailTemplate(
            template_name=file_name,
            platform=platform,
            company=company,
            file_id=file_id,
            folder_id=folder_id,
            subject = content['subject'],
            body = content['body'],
            date_created = datetime.now(),
        )
        print(f"Db file info: {file}")
        file.save()
        print("File saved successfully")
        return True
    except Exception as e:
        print(f"Error saving file info: {e}")
        return False