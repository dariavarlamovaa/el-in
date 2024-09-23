from django.shortcuts import render
from django.views.generic import TemplateView

from places.forms import PlaceSelectorForm


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PlaceSelectorForm()
        context.update({'form': form})
        return context