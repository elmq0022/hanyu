
'''
This module is the base command for parsing the CC-CEDIct Chinese to English dictionary located
at https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip
'''

import io
import re
import zipfile

import requests
from django.core.management.base import BaseCommand, CommandError


class BaseCEDictCommand(BaseCommand):

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
        (?P<pin_yin>[a-z:,\d\s]+)           # pronunc pattern
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
