from django.views.generic import TemplateView

from places.token import make_api_request


class PlaceView(TemplateView):
    template_name = 'places/places.html'


class OneHikingPlaceView(TemplateView):
    pass
