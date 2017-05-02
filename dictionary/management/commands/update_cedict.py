
'''
This module will update the Entry table using the CC-CEDIct Chinese to English dictionary located
at https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip

*** For now making the assumption that a word or phrase will not be removed from the database ***
*** For now also assuming there won't be changes to entries provided the database is maintained regularly ***

TODO: There is a ton of code duplication here.  I should look at refactoring this. Just want to get it running right now.
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
        pattern = r'''
        (?P<traditional>\w+)                # first character
        \s+                                 # spaces
        (?P<simple>\w+)                     # second character
        \s+                                 # spaces
        \[                                  # start pronunc
        (?P<pin_yin>[a-z\d\s:,]+)             # pronunc pattern
        \]                                  # end pronunc
        \s+                                 # spaces
        /                                   # start the defintions 
        (?P<definitions>.+)                 # definitions
        /                                   # end the defintions 
        '''
        self.valid_entries = re.compile(pattern, re.M|re.I|re.X)
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

    def update_db(self, matches):
        updated, added = 0, 0
        entries = []
        all_entries = {e.simple + e.traditional + e.pin_yin : (e.pk, e.definitions)
                       for e in models.Entry.objects.all()}
        for match in matches:
            key = match['simple'] + match['traditional'] + match['pin_yin']
            if key not in all_entries:
                entry = models.Entry(
                    traditional=match['traditional'],
                    simple=match['simple'],
                    pin_yin=match['pin_yin'],
                    definitions=self.slash.sub(r' / ', match['definitions'])
                )
                entries.append(entry)
                added += 1
            elif all_entries[key][1] != self.slash.sub(r' / ', match['definitions']):
                entry = models.Entry.objects.get(all_entries[key][0])
                entry.definitions = self.slash.sub(r' / ', match['definitions'])
                entry.save()
                updated += 1
        models.Entry.objects.bulk_create(entries)
        return updated, added

    def handle(self, *args, **options):
        print("Downloading dictionary from {}.".format(self.url))
        text = self.download_dict()
        print("Download complete.")

        print("Entering data into database.")
        matches = self.valid_entries.finditer(text)
        updated, added = self.update_db(matches)

        print("Complete. The database had {} entries updated and {} added.".format(updated, added))
