'''
This module will load the Entry table using the CC-CEDIct Chinese to English dictionary located
at https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip
'''

from django.core.management.base import BaseCommand, CommandError

from dictionary import models
from ._base_cedict import BaseCEDictCommand


class Command(BaseCEDictCommand):
    help = 'loads the online version of CC-CEDICT Chinese to English dictionary into the database'

    def add_to_db(self, matches):
        count = 0
        entries = []

        for match in matches:
            entry = models.Entry(
                traditional=match['traditional'],
                simple=match['simple'],
                pin_yin=match['pin_yin'],
                definitions=self.slash.sub(r' / ', match['definitions'])
            )
            entries.append(entry)
            count += 1

        models.Entry.objects.bulk_create(entries)
        return count

    def handle(self, *args, **options):
        print("Downloading dictionary from {}.".format(self.url))
        text = self.download_dict()
        print("Download complete.")

        print("Deleting entries from database.")
        models.Entry.objects.all().delete()

        print("Entering data into database.")
        matches = self.valid_entries.finditer(text)
        count = self.add_to_db(matches)

        print("Complete. There were {} entries entered into the database.".format(count))
