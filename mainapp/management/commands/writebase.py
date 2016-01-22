from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Metka

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('text', nargs='+', type=str)

    def handle(self, *args, **options):
        metka = Metka(text='poll_id')
        metka.save()
        self.stdout.write(self.style.SUCCESS('successful written "%s"' % text))