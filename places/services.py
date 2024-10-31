import os
import json
import requests

from decimal import Decimal
from collections import defaultdict

from django.core.files.base import ContentFile
from django.db.models.functions import Collate
from dotenv import load_dotenv

from django.http import JsonResponse
from django.db.models import Q
from django.utils.translation import get_language

from django.conf import settings
from places.models import Place

load_dotenv()


class DataHubAPI:
    @staticmethod
    def get_api_data_for_datahub():
        url = 'https://iam-datahub.visitfinland.com/auth/realms/Datahub/protocol/openid-connect/token'

        access_data = {
            'client_id': 'datahub-api',
            'client_secret': f'{os.getenv("SECRET_KEY")}',
            'grant_type': 'password',
            'username': f'{os.getenv("USERNAME")}',
            'password': f'{os.getenv("DH_PASSWORD")}'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return url, access_data, headers

    def get_access(self):
        url, access_data, headers = self.get_api_data_for_datahub()
        try:
            response = requests.post(url, data=access_data, headers=headers)
            access_token = response.json().get('access_token')
            return access_token
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_api_data_for_graphql_query(self, query):
        request_url = 'https://api-datahub.visitfinland.com/graphql/v1/graphql'
        access_token = self.get_access()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        body = {
            'query': query,
        }
        return request_url, headers, body

    @staticmethod
    def get_query():
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
        return query

    def make_api_request(self):
        request_url, headers, body = self.get_api_data_for_graphql_query(self.get_query())
        try:
            response = requests.post(request_url, headers=headers, data=json.dumps(body))
            response_data = response.json()
            return response_data
        except Exception as e:
            return JsonResponse(f"Error getting access token: {e}", status=400)

    def save_data(self, filename):
        with open(filename, 'w') as f:
            data = self.make_api_request()
            json.dump(data, f)


# test = DataHubAPI()
# test.save_data('test.json')


# clear all data by searching for english and finnish data and deleting another languages data
class DataFromDataHub:
    def get_data_from_file(self, filename):
        if Place.objects.exists():
            print("Data has already been loaded. Aborting import.")
            return
        else:
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
                    location = product['postalAddresses'][0]['location'][1:-1].split(',')
                    latitude = Decimal(location[0])
                    longitude = Decimal(location[1])
                    postal_code = product['postalAddresses'][0]['postalCode']
                    street_name = product['postalAddresses'][0]['streetName']
                    city = product['postalAddresses'][0]['city']

                    # time for visiting info
                    available_time = ', '.join([month['month'] for month in product['productAvailableMonths']])

                    # price info
                    price = 'Free' if (
                            product['productPricings'][0]['fromPrice'] == 0.0 and product['productPricings'][0][
                        'toPrice'] == 0.0) else f'Paid'

                    self.insert_data_into_table(image_path, image_alt_text, image_url, description_eng, name_eng, url,
                                                description_fin, name_fin, latitude, longitude, postal_code,
                                                street_name,
                                                city, available_time, price)

    @staticmethod
    def insert_data_into_table(image_path, image_alt_text, image_url, description_eng, name_eng, url,
                               description_fin, name_fin, latitude, longitude, postal_code, street_name, city,
                               available_time, price):
        response = requests.get(image_url)

        if response.status_code == 200:
            place = Place(
                image_alt_text=image_alt_text,
                image_url=image_url,
                description_eng=description_eng,
                name_eng=name_eng,
                url=url,
                description_fin=description_fin,
                name_fin=name_fin,
                latitude=latitude,
                longitude=longitude,
                postal_code=postal_code,
                street_name=street_name,
                city=city,
                available_time=available_time,
                price=price
            )

            image_name = image_path
            place.image.save(image_name, ContentFile(response.content), save=True)


def get_cities_and_places(filter_data=None):
    lang = get_language()
    if lang == 'en':
        places_data = (Place.objects.filter(filter_data).values('id', 'city', 'name_eng', 'image',
                                                                'available_time').order_by(Collate("city", "fi-x-icu"),
                                                                                           'name_eng'))
    elif lang == 'fi':
        places_data = Place.objects.filter(filter_data).values('id', 'city', 'name_fin', 'image',
                                                               'available_time').order_by(Collate("city", "fi-x-icu"),
                                                                                          'name_fin')
    else:
        places_data = {}
    cities_and_places = defaultdict(list)
    for item in places_data:
        cities_and_places[item['city']].append(
            {'id': item['id'], 'name': item['name_eng'] if lang == 'en' else item['name_fin'],
             'image': f"{settings.MEDIA_URL}{item['image']}",
             'available_time': item['available_time']})
    cities_and_places = dict(cities_and_places)
    return cities_and_places


def filter_cities_places(city=None, month=None, price=None):
    filter_data = Q()
    if city:
        filter_data &= Q(city=city)
    if month:
        filter_data &= Q(available_time__icontains=month)
    if price:
        filter_data &= Q(price__icontains=price)
    return get_cities_and_places(filter_data)


class WeatherAPI:

    @staticmethod
    def get_api_for_current_weather():
        api_key = os.getenv('WEATHER_API_KEY')
        return api_key

    @staticmethod
    def get_current_weather(lat, lon):
        lang = get_language()
        api_key = WeatherAPI.get_api_for_current_weather()
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={lang}&units=metric'
        try:
            response = requests.get(url, timeout=3).json()
            weather_parameter = response['weather'][0]['description'].lower()
            temp = round(response['main']['temp'])
            icon = response['weather'][0]['icon']
            icon_path = f'https://openweathermap.org/img/wn/{icon}.png'
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

        return weather_parameter, temp, icon_path


def get_places_for_main_map():
    lang = get_language()
    if lang == 'en':
        places_data = list(Place.objects.all().values('id', 'city', 'name_eng', 'image', 'latitude', 'longitude'))
    elif lang == 'fi':
        places_data = list(Place.objects.all().values('id', 'city', 'name_fin', 'image', 'latitude', 'longitude'))
    else:
        places_data = list({})

    renamed_places_data = []
    for place in places_data:
        place['image'] = f"{settings.MEDIA_URL}{place['image']}"
        place['name'] = place.pop('name_eng' if lang == 'en' else 'name_fin')
        renamed_places_data.append(place)

    return renamed_places_data
