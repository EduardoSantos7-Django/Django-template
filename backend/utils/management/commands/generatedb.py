from django.core.management.base import BaseCommand, CommandError, CommandParser

from utils.db import generate_db


class Command(BaseCommand):
    help = 'Generate a random database'

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        generate_db()
