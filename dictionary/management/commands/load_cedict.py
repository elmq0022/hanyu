'''
This module will load the Entry table using the CC-CEDIct Chinese to English dictionary located
at https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip
'''

import io
import re
import zipfile

import requests
from django.core.management.base import BaseCommand, CommandError

from dictionary import models


class Command(BaseCommand):
    help = 'loads the online version of CC-CEDICT Chinese to English dictionary into the database'

    def __init__(self):
        super().__init__()
        '''
        The CC-CEDICT dictionary is a work in progress.
        The following regex pattern will match all well formed entries in the dictionary
        '''
        entry_pattern = r'''
        (?P<traditional>\w+)                # first character
        \s+                                 # spaces
        (?P<simple>\w+)                     # second character
        \s+                                 # spaces
        \[                                  # start pronunc
        (?P<pin_yin>[a-z:\d\s]+)             # pronunc pattern
        \]                                  # end pronunc
        \s+                                 # spaces
        /                                   # start the defintions 
        (?P<definitions>.+)                 # definitions
        /                                   # end the defintions 
        '''

        self.valid_entries = re.compile(entry_pattern, re.M|re.I|re.X)
        self.slash = re.compile(r'/')

        self.url = r'https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip'

    def download_dict(self):
        '''
        Download Chinese-English dictionary zip file and return the contents as a string.
        '''
        r = requests.get(self.url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        file_name = z.namelist()[0]
        with z.open(file_name) as f:
            text = f.read().decode("utf-8")
        return text

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
