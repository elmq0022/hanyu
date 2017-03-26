import io
import re
import requests
import zipfile
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
        (?P<pin_yin>[a-z\d\s]+)             # pronunc pattern
        \]                                  # end pronunc
        \s+                                 # spaces
        (?P<english_equivalents>/.+/)       # definitions
        '''
        self.valid_entries = re.compile(pattern, re.M|re.I|re.X)

    def download_dict(self):
        '''
        Download dictionary zip file from ??? and return the contents as a string
        '''
        url = r'https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip'
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        file_name = z.namelist()[0]
        f = z.open(file_name)
        text = f.read().decode("utf-8")
        return text

    def add_arguments(self, parser):
        pass

    def add_to_db(self, matches):
        count = 0
        for i, match in enumerate(matches):
            entry = models.Entry(
                traditional=match['traditional'],
                simple=match['simple'],
                pronunciation=match['pin_yin'],
                order=i
            )
            entry.save()
            count += 1
            for j, item in enumerate(match['english_equivalents'].split('/')):
                definition = models.Definition(
                    entry=entry,
                    order=j,
                    text=item
                )
                definition.save()

        print(count)

    def handle(self, *args, **options):
        text = self.download_dict()
        matches = self.valid_entries.finditer(text)
        self.add_to_db(matches)
        print('done')
