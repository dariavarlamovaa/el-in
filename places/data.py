import json
import os

import requests
from django.http import JsonResponse
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


def save_data(query, filename):
    with open(filename, 'w') as f:
        data = make_api_request(query)
        json.dump(data, f)


def get_all_products_data():
    query = """ {
                product (where: {
                    _and: [
                        {type:{_eq:attraction}},
                        {productTags:{tag:{_eq:"hiking_walking_trekking"}}},
                        {productTargetGroups:{targetGroupId:{_eq:b2c}}},
                    ]}){
                    productImages {
                        filename
                        altText
                        largeUrl
                    }
                    productInformations {
                        description
                        name
                        url
                    }
                    postalAddresses {
                        location
                        postalCode
                        streetName
                        city
                    }
                    productAvailableMonths{
                        month
                    }
                    productPricings {
                        fromPrice
                        toPrice
                    }
                }
            }"""
    save_data(query, 'data.json')


# clear all data by searching for english and finnish data and deleting another languages data

def save_data_in_table(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        for product in data['product']:
            # image info
            image_path = product['productImages'][0]['filename']
            image_alt_text = product['productImages'][0]['altText'].strip() if product['productImages'][0][
                                                                                   'altText'] is not None else 'Product image'
            image_url = product['productImages'][0]['largeUrl']

            # product info in english
            description_eng = product['productInformations'][0]['description']
            name_eng = product['productInformations'][0]['name']
            url = product['productInformations'][0]['url'] if product['productInformations'][0]['url'] else \
                product['productInformations'][1]['url']

            # product info in finnish
            description_fin = product['productInformations'][1]['description']
            name_fin = product['productInformations'][1]['name']

            # location info
            location = product['postalAddresses'][0]['location']
            postal_code = product['postalAddresses'][0]['postalCode']
            street_name = product['postalAddresses'][0]['streetName']
            city = product['postalAddresses'][0]['city']

            # time for visiting info
            available_time = 'All year' if len(product['productAvailableMonths']) == 12 else ', '.join(
                [month['month'] for month in product['productAvailableMonths']])

            # price info
            price = 'Free' if (product['productPricings'][0]['fromPrice'] == 0.0 and product['productPricings'][0][
                'toPrice'] == 0.0) else f'Paid (€)'

            # print(image_path)
            # print(image_alt_text)
            # print(image_url)
            # print(description_eng)
            # print(name_eng)
            # print(url)
            # print(description_fin)
            # print(name_fin)
            # print(location)
            # print(postal_code)
            # print(street_name)
            # print(city)
            # print(available_time)
            # print(price)


save_data_in_table('data.json')
