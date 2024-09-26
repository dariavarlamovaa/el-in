from collections import defaultdict

from django.db.models import Q

from places.models import Place


def get_cities_and_places(city=None, month=None):
    filter_data = Q()
    if city:
        filter_data &= Q(city=city)
    if month:
        filter_data &= Q(available_time__icontains=month)
    places_data = Place.objects.filter(filter_data).values('id', 'city', 'name_eng', 'image_path',
                                                           'available_time').order_by(
        'city', 'name_eng')
    cities_and_places = defaultdict(list)
    for item in places_data:
        cities_and_places[item['city']].append(
            {'id': item['id'], 'name_eng': item['name_eng'], 'image_path': item['image_path'],
             'available_time': item['available_time']})
    cities_and_places = dict(cities_and_places)
    return cities_and_places
