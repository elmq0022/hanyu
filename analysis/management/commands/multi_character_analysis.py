import os
from collections import Counter
from string import ascii_letters, digits, punctuation, whitespace

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from lxml import html
from nltk.tokenize import stanford_segmenter

from analysis.models import Count
from dictionary.models import Entry


class Command(BaseCommand):
    help = '''
    parse a list of documents and bag the occurences of dictionary entries.  
    '''

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ['JAVAHOME'] = settings.JAVAHOME
        os.environ['CLASSPATH'] = settings.CLASSPATH
        self.segmenter = stanford_segmenter.StanfordSegmenter(**settings.STFORD_SEG_SETTINGS)
        self.entries = {e.simple: e for e in Entry.objects.all()}
        super().__init__()

    def extract_text_from_html(self, file_path=None, encoding='utf-8'):
        file_path = os.path.join(self.base_dir, 'resources', 'wiki_zh_china.xml') #TODO: Fix this!
        with open(file_path, encoding="utf-8") as f:
            article = f.read()
        tree = html.fromstring(article)
        content = tree.xpath(r'//*[@id="mw-content-text"]//text()')
        return ''.join(content)

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
        results = self.segmenter.segment(content).split()
        self.word_counts.update(Counter(results))

    def load_to_db(self, counts, count_type):
        records = []
        for phrase, count in counts.items():
            if phrase in self.entries:
                records.append(Count(entry=self.entries[phrase],
                                     count=count,
                                     count_type=count_type
                                    )
                              )
        Count.objects.bulk_create(records)

    def handle(self, *args, **options):
        self.set_character_counts()
        self.set_word_counts()

        # for file in files:  TODO: make this a loop for a directory of files...
        content = self.extract_text_from_html()
        self.update_character_counts(content)
        self.update_word_counts(content)

        #Delete
        Count.objects.all().delete()

        #Load
        self.load_to_db(self.character_counts, Count.CHARACTER)
        self.load_to_db(self.word_counts, Count.WORD)
