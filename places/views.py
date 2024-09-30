from django.views.generic import ListView, DetailView

from .forms import PlaceSelectorForm
from .models import Place
from .services import get_cities_and_places, WeatherAPI


class PlaceView(ListView):
    form = PlaceSelectorForm()
    template_name = 'places/places.html'

    def get_queryset(self):
        cities_and_places = get_cities_and_places()
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
        cities_and_places = get_cities_and_places(selected_city, selected_month)
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
                'id', 'image_path', 'image_alt_text', 'description_eng',
                'name_eng', 'url', 'latitude', 'longitude', 'postal_code',
                'street_name', 'city', 'available_time', 'price'
            )
        elif lang == 'fi':
            return Place.objects.values(
                'id', 'image_path', 'image_alt_text', 'description_fin', 'name_fin', 'url', 'latitude', 'longitude',
                'postal_code', 'street_name', 'city', 'available_time', 'price'
            )
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = self.get_object()

        best_time_to_visit = place['available_time'].split(', ')
        if len(best_time_to_visit) == 12:
            available_time = 'All year'
        else:
            first_month = best_time_to_visit[0][:3].title()
            last_month = best_time_to_visit[-1][:3].title()
            available_time = f'{first_month} - {last_month}'

        weather_parameter, temp, icon_path = WeatherAPI.get_current_weather(place['latitude'], place['longitude'])

        lang = self.request.LANGUAGE_CODE
        name = place['name_eng'] if lang == 'en' else place['name_fin']
        description = place['description_eng' if lang == 'en' else 'description_fin']
        description_list = [s.strip() for s in description.split('\n') if s.strip()]

        context.update(
            {'place': place, 'available_time': available_time, 'weather_parameter': weather_parameter, 'name': name,
             'description': description_list, 'temp': temp, 'icon_path': icon_path})
        return context
