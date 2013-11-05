from django.core.management.base import BaseCommand
from stampu.renderers.disk import Renderer


class Command(BaseCommand):
    help = "Generates static content based on the site configuration."

    def handle(self, *args, **options):
        print("=> Starting conversion")
        renderer = Renderer()
        renderer.add_path('/')
        renderer.start()
