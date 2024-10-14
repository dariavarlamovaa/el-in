from django import forms
from django.db import connection

from places.models import Place


class PlaceSelectorForm(forms.Form):
    months = [
        ('january', 'January'), ('february', 'February'), ('march', 'March'),
        ('april', 'April'), ('may', 'May'), ('june', 'June'),
        ('july', 'July'), ('august', 'August'), ('september', 'September'),
        ('october', 'October'), ('november', 'November'), ('december', 'December')]
    model = Place
    city = forms.ChoiceField(required=False)
    month = forms.ChoiceField(choices=months, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'places_place' in connection.introspection.table_names():
            city_choices = [(city, city) for city in
                            Place.objects.values_list('city', flat=True).order_by('city').distinct()]
        else:
            city_choices = ['No cities', 'No cities'],
        self.fields['city'].choices = city_choices
