from django.core.management.base import BaseCommand
from django.core import serializers

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('data.json', 'r', encoding='utf-8') as json_file:
            json_data = json_file.read()
            for obj in serializers.deserialize('json', json_data):
                obj.save()
        self.stdout.write(self.style.SUCCESS('Data successfully loaded from data.json'))