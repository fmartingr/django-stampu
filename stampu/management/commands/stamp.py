from django.core.management.base import BaseCommand
from stampu.renderers.disk import DiskRenderer


class Command(BaseCommand):
    help = "Generates static content based on the site configuration."

    def handle(self, *args, **options):
        # TODO get save path from argument

        print("=> Converting all your site into static content")

        renderer = DiskRenderer()

        renderer.add_path('/')

        renderer.start()
