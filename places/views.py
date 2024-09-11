from django.shortcuts import render
from django.views.generic import TemplateView


class PlaceView(TemplateView):
    template_name = 'places/places.html'