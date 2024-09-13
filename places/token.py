import json
import os

import requests
from django.http import JsonResponse, HttpResponse
from dotenv import load_dotenv

load_dotenv()


def get_access():
    url = 'https://iam-datahub.visitfinland.com/auth/realms/Datahub/protocol/openid-connect/token'

    access_data = {
        'client_id': 'datahub-api',
        'client_secret': f'{os.getenv("SECRET_KEY")}',
        'grant_type': 'password',
        'username': f'{os.getenv("USERNAME")}',
        'password': f'{os.getenv("PASSWORD")}'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=access_data, headers=headers)
        access_token = response.json().get('access_token')
        return access_token
    except Exception as e:
        return JsonResponse(f"Error getting access token: {e}", status=400)


def make_api_request(query):
    request_url = 'https://api-datahub.visitfinland.com/graphql/v1/graphql'
    access_token = get_access()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    body = {
        'query': query,
    }

    try:
        response = requests.post(request_url, headers=headers, data=json.dumps(body))
        response_data = response.json()
        return response_data
    except Exception as e:
        return JsonResponse(f"Error getting access token: {e}", status=400)
