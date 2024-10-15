from django import forms
from django.db import connection
from django.db.models.functions import Collate
from django.utils.translation import get_language

from places.models import Place


class PlaceSelectorForm(forms.Form):
    months_eng = [
        ('january', 'January'), ('february', 'February'), ('march', 'March'),
        ('april', 'April'), ('may', 'May'), ('june', 'June'),
        ('july', 'July'), ('august', 'August'), ('september', 'September'),
        ('october', 'October'), ('november', 'November'), ('december', 'December')]
    months_fin = [
        ('january', 'Tammikuu'), ('february', 'Helmikuu'), ('march', 'Maaliskuu'), ('april', 'Huhtikuu'),
        ('may', 'Toukokuu'), ('june', 'Kesäkuu'), ('july', 'Heinäkuu'), ('august', 'Elokuu'),
        ('september', 'Syyskuu'), ('october', 'Lokakuu'), ('november', 'Marraskuu'), ('december', 'Joulukuu')]
    city = forms.ChoiceField(required=False)
    month = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_language = get_language()
        if current_language == 'en':
            self.fields['month'].choices = self.months_eng
        else:
            self.fields['month'].choices = self.months_fin

        if 'places_place' in connection.introspection.table_names():
            city_choices = [(city, city) for city in
                            Place.objects.values_list('city', flat=True).order_by(
                                Collate("city", "fi-x-icu")).distinct()]
        else:
            city_choices = ['No cities', 'No cities'],
        self.fields['city'].choices = city_choices
