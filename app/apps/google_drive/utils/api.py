import requests
import json
from django.http import JsonResponse

def create_drive_folder(access_token):
    # Google Drive API endpoint URL for creating a folder
    create_folder_url = 'https://www.googleapis.com/drive/v3/files'

    # Headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Payload for creating the folder
    folder_metadata = {
        'name': 'SuperFunnel CRM',
        'mimeType': 'application/vnd.google-apps.folder',
    }

    # Make a POST request to create the folder
    response = requests.post(create_folder_url, json=folder_metadata, headers=headers)

    if response.status_code == 200:
        # Parse the response
        folder_data = response.json()
        print(f"folder_data: {folder_data}")

        return folder_data
    
    elif response.status_code == 401:
        raise AuthenticationError("Authentication failed")


class AuthenticationError(Exception):
    pass

def create_file_template(access_token, folder_id, name, content):
    # Google Drive API endpoint URL for creating a document
    create_doc_url = 'https://www.googleapis.com/drive/v3/files'

    # Headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Payload for creating the document
    doc_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id],
    }

    # Create the document
    response = requests.post(create_doc_url, json=doc_metadata, headers=headers)
    print(f"response: {response.text}")
    print(f"response.status_code: {response.status_code}")

    if response.status_code == 200:
        doc_data = response.json()
        print(f"doc_data: {doc_data}")
        print(f"file id again: {doc_data.get('id', '')}")
        file_id = doc_data.get('id', '')

        # Update the document content
        update_url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}"
        print(f"update_url: {update_url}")
        file_data = {
            'content': content
        }
        update_response = requests.patch(update_url, headers=headers, json=file_data)

        print(f"update_response: {update_response.status_code}")
        print(f"update_response.text: {update_response.text}")
        if update_response.status_code == 200:
            
            return file_id
    elif response.status_code == 401:
        raise AuthenticationError("Authentication failed")
    

    return JsonResponse({'success': False, 'error': 'Failed to create document'})
