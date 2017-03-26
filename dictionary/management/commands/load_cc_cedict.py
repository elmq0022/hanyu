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
        /                                   # start the english equivalents
        (?P<english_equivalents>.+)         # definitions
        /                                   # end the english equivalents
        '''
        self.valid_entries = re.compile(pattern, re.M|re.I|re.X)
        self.url = r'https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip'

    def download_dict(self):
        '''
        Download dictionary zip file from ??? and return the contents as a string
        '''
        r = requests.get(self.url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        file_name = z.namelist()[0]
        f = z.open(file_name)
        text = f.read().decode("utf-8")
        return text

    def add_arguments(self, parser):
        pass

    def delete_entries_from_db(self):
        models.Definition.objects.all().delete()
        models.Entry.objects.all().delete()

    def add_to_db(self, matches):
        count = 0
        entries = []
        definitions = []

        for i, match in enumerate(matches):
            entry = models.Entry(
                traditional=match['traditional'],
                simple=match['simple'],
                pronunciation=match['pin_yin'],
                order=i
            )
            entries.append(entry)
            count += 1

        models.Entry.objects.bulk_create(entries)

        for i, match in enumerate(matches):
            for j, item in enumerate(match['english_equivalents'].strip().split('/')):
                definition = models.Definition(
                    entry_id=i,
                    order=j,
                    text=item
                )
                definitions.append(definition)

        models.Definition.objects.bulk_create(definitions)
        print("There were {} entries inserted into the database".format(count))

    def handle(self, *args, **options):
        print("Downloading dictionary from {}".format(self.url))
        text = self.download_dict()
        print("Download complete")

        print("Deleting entries from database")
        self.delete_entries_from_db()        
        
        print("Entering data into database")
        matches = list(self.valid_entries.finditer(text))
        self.add_to_db(matches)
        print('done')
