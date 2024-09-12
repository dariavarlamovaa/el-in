import os

import requests
from django.http import JsonResponse, HttpResponse


def get_access(request):
    url = 'https://iam-datahub.visitfinland.com/auth/realms/Datahub/protocol/openid-connect/token'

    access_data = {
        'client_id': 'datahub-api',
        'client_secret': f'{os.getenv("SECRET_KEY")}',
        'grant_type': 'password',
        'username': f'{os.getenv("USERNAME")}',
        'password': f'{os.getenv("PASSWORD")}'
    }

    try:
        response = requests.post(url, data=access_data)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        return access_token
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error getting access token: {e}", status=500)


def make_api_request(request):
    request_url = 'https://api-datahub.visitfinland.com/graphql/v1/graphql'
    access_token = get_access(request)
    print(access_token)

    if not access_token:
        return HttpResponse("Failed to retrieve access token", status=500)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(request_url, headers=headers)
        response_data = response.json()
        return JsonResponse(response_data)
    except Exception as e:
        return e


