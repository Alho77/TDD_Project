import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self):
        """Django command to pause execution until database is available"""
        # FIXME: why style aren't working
        # self.stdout.write(self.style.WARNING('Waiting for db ...'))
        self.stdout.write('Waiting for db ...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                # self.stdout.write(self.style.ERROR(
                #     'DB is unavailable, waiting for 1 sec ...'))
                self.stdout.write('DB is unavailable, waiting for 1 sec ...')
                time.sleep(1)

        # self.stdout.write(self.style.success('DB is available!'))
        self.stdout.write('DB is available!')
