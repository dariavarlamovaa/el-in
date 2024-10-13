from django.core.management.base import BaseCommand
from places.services import DataFromDataHub


class Command(BaseCommand):
    help = 'Import data from file into the database'

    def handle(self, *args, **kwargs):
        filename = 'places/data.json'
        data_loader = DataFromDataHub()
        data_loader.get_data_from_file(filename)
