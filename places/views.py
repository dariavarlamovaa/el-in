from django.views.generic import TemplateView

class PlaceView(TemplateView):
    template_name = 'places/places.html'


class OneHikingPlaceView(TemplateView):
    pass
