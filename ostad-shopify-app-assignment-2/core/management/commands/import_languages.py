from django.core.management.base import BaseCommand
from core.models import Language
import csv


class Command(BaseCommand):
    help = "Script to import langauge data from csv file to db"

    def handle(self, *args, **kwargs):

        with open(
            "core/data/languages.csv", "r"
        ) as language_file:
            language_data = csv.reader(language_file)

            for row in language_data:
                db_row = Language(name=row[0], code=row[1])
                db_row.save()
                print(f"Imported language {db_row}")