import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Django command to pause execution until database is available"""
        self.stdout.write(self.style.WARNING('Waiting for db ...'))
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(self.style.ERROR(
                    'DB is unavailable, waiting for 1 sec ...'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB is available!'))
