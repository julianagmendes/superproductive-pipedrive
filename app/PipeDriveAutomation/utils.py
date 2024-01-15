import requests
import json
import os
import boto3
from botocore.exceptions import ClientError, ExpiredTokenException

# def get_secret_dict(secret_name):
#     region_name = "us-east-2"
#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )
#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=f"superproductive/superfunnel/{secret_name}"
#         )
#     except ClientError as e:
#         raise e
    
#     secret = get_secret_value_response['SecretString']
#     secret_dict = json.loads(secret)
#     return secret_dict



def get_secret_dict(secret_name):
    region_name = "us-east-2"
    
    # Create a Boto3 session
    session = boto3.session.Session()
    
    while True:
        try:
            # Access the client using the session
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )

            # Get the secret value
            get_secret_value_response = client.get_secret_value(
                SecretId=f"superproductive/superfunnel/{secret_name}"
            )

            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            return secret_dict
        
        except ExpiredTokenException:
            # Refresh the credentials and retry
            session.get_credentials().refresh()

