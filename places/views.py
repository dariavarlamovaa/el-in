from django.views.generic import ListView, DetailView, TemplateView

from finnhike import settings
from .forms import PlaceSelectorForm
from .models import Place
from .services import WeatherAPI, filter_cities_places, get_places_for_main_map


class PlaceView(ListView):
    form = PlaceSelectorForm()
    template_name = 'places/places.html'

    def get_queryset(self):
        cities_and_places = filter_cities_places()
        return cities_and_places

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities_and_places = self.get_queryset()
        context.update({'cities_and_places': cities_and_places, 'form': self.form})
        return context


class PlaceFilter(ListView):
    template_name = 'places/places.html'
    form = PlaceSelectorForm()

    def get_queryset(self):
        selected_city = self.request.GET.get('city_selector', None)
        selected_month = self.request.GET.get('month_selector', None)
        cities_and_places = filter_cities_places(selected_city, selected_month)
        return cities_and_places

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cities_and_places = self.get_queryset()
        context.update({'cities_and_places': cities_and_places, 'form': self.form})
        return context


class HikingPlaceView(DetailView):
    template_name = 'places/place.html'
    model = Place
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        if lang == 'en':
            return Place.objects.values(
                'id', 'image', 'image_alt_text', 'description_eng',
                'name_eng', 'url', 'latitude', 'longitude', 'postal_code',
                'street_name', 'city', 'available_time', 'price'
            )
        elif lang == 'fi':
            return Place.objects.values(
                'id', 'image', 'image_alt_text', 'description_fin', 'name_fin', 'url', 'latitude', 'longitude',
                'postal_code', 'street_name', 'city', 'available_time', 'price'
            )
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lang = self.request.LANGUAGE_CODE

        months = {'january': 'tammikuu', 'february': 'helmikuu', 'march': 'maaliskuu', 'april': 'huhtikuu',
                  'may': 'toukokuu', 'june': 'kesäkuu', 'july': 'heinäkuu', 'august': 'elokuu', 'september': 'syyskuu',
                  'october': 'lokakuu', 'november': 'marraskuu', 'december': 'joulukuu'}

        place = self.get_object()

        best_time_to_visit = place['available_time'].split(', ')
        if len(best_time_to_visit) == 12:
            available_time = 'All year' if lang == 'en' else 'Ympäri vuoden'
        else:
            first_month_in_list = best_time_to_visit[0]
            last_month_in_list = best_time_to_visit[-1]
            first_month = first_month_in_list if lang == 'en' else months.get(first_month_in_list)
            last_month = last_month_in_list if lang == 'en' else months.get(last_month_in_list)
            available_time = f'{first_month.title()} - {last_month.title()}'

        weather_parameter, temp, icon_path = WeatherAPI.get_current_weather(place['latitude'], place['longitude'])

        image = f"{settings.MEDIA_URL}{place['image']}"
        name = place['name_eng'] if lang == 'en' else place['name_fin']
        description = place['description_eng' if lang == 'en' else 'description_fin']
        description_list = [s.strip() for s in description.split('\n') if s.strip()]

        latitude = place['latitude']
        longitude = place['longitude']

        context.update(
            {'place': place, 'image': image, 'available_time': available_time, 'weather_parameter': weather_parameter,
             'name': name, 'description': description_list, 'latitude': latitude, 'longitude': longitude, 'temp': temp,
             'icon_path': icon_path})
        return context


class Map(ListView):
    template_name = 'places/map.html'

    def get_queryset(self):
        places = get_places_for_main_map()
        return places

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        places = self.get_queryset()
        context.update({'places': places})
        return context


class HikingTip(TemplateView):
    template_name = 'places/hiking_tips.html'
