import glob
import os
from collections import Counter
from string import ascii_letters, digits, punctuation, whitespace

import jieba
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from lxml import html
from nltk.tokenize import stanford_segmenter

from analysis.models import Count
from dictionary.models import Entry


class Command(BaseCommand):
    help = '''
    Parse a list of documents and bag the occurences of dictionary entries.  
    '''

    def __init__(self):
        # os.environ['JAVAHOME'] = settings.JAVAHOME
        # os.environ['CLASSPATH'] = settings.CLASSPATH
        # self.segmenter = stanford_segmenter.StanfordSegmenter(**settings.STFORD_SEG_SETTINGS)
        super().__init__()


    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            nargs='+',
            dest='path_or_file',
            help='Segment a file or directory of files and add the occurences to the Count table'
        )
        parser.add_argument(
            '-e',
            '--extension',
            default='',
            dest='extension',
            help='File extension to filter by'
        )
        parser.add_argument(
            '-D',
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete all the items from the Count table'
        )

    def extract_text_from_html(self, file_path=None, encoding='utf-8'):
        with open(file_path, encoding="utf-8") as f:
            article = f.read()
        tree = html.fromstring(article)
        content = tree.xpath(r'//*[@id="mw-content-text"]//text()') # TODO: This shouldn't be hard-coded...
        return ' '.join(content)

    def set_character_counts(self):
        character_counts = Count.objects.filter(count_type=Count.CHARACTER).all()
        self.character_counts = Counter({item.entry.simple: item.count for item in character_counts})

    def update_character_counts(self, content):
        content = ''.join(content)
        exclude = whitespace + digits + ascii_letters + punctuation
        single_chars = [i for i in content if i not in exclude]
        self.character_counts.update(Counter(single_chars))

    def set_word_counts(self):
        word_counts = Count.objects.filter(count_type=Count.WORD).all()
        self.word_counts = Counter({item.entry.simple: item.count for item in word_counts})

    def update_word_counts(self, content):
        segments = jieba.cut(content)
        # results = self.segmenter.segment(content).split()
        self.word_counts.update(Counter(segments))

    def load_to_db(self, counts, count_type, entries):
        records = []
        for item, count in counts.items():
            if item in entries:
                records.append(Count(entry=entries[item],
                                     count=count,
                                     count_type=count_type
                                    )
                              )
        Count.objects.bulk_create(records)

    def handle(self, *args, **options):
        if options['path_or_file']:
            self.set_character_counts()
            self.set_word_counts()

            full_paths = [os.path.join(os.getcwd(), path) for path in options['path_or_file']]
            files = set()
            for path in full_paths:
                if os.path.isfile(path):
                    files.add(path)
                else:
                    files |= set(glob.glob(path + '/*' + options['extension']))

            for file in files:
                content = self.extract_text_from_html(file)
                self.update_character_counts(content)
                self.update_word_counts(content)

            # Delete all records
            Count.objects.all().delete()

            # Use bulk load to update
            entries = {e.simple: e for e in Entry.objects.all()}
            self.load_to_db(self.character_counts, Count.CHARACTER, entries)
            self.load_to_db(self.word_counts, Count.WORD, entries)

        if options['delete']:
            ans = input('Drop all entries from the Count table [Y]/n: ').lower()
            if ans == 'y' or ans == '':
                Count.objects.all().delete()
