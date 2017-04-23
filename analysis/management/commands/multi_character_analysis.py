import os
from collections import Counter
from string import ascii_letters, digits, punctuation, whitespace

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Length
from lxml import html
from nltk.tokenize import stanford_segmenter

from analysis.models import SingleCount, MultiCount
from dictionary.models import Entry


class Command(BaseCommand):
    help = '''
    parse a list of html documents and bag the occurence of dictionary entries.  
    '''

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ['JAVAHOME'] = settings.JAVAHOME
        os.environ['CLASSPATH'] = settings.CLASSPATH
        self.segmenter = stanford_segmenter.StanfordSegmenter(
            path_to_jar=settings.STFD_SEG,
            path_to_slf4j=settings.SLF4J,
            path_to_sihan_corpora_dict=settings.SIHAN_DICT,
            path_to_model=settings.MODEL,
            path_to_dict=settings.DICT
            )
        self.entries = {e.simple: e for e in Entry.objects.all()}
        super().__init__()

    def extract_text_from_html(self, file_path=None, encoding='utf-8'):
        file_path = os.path.join(self.base_dir, 'resources', 'wiki_zh_china.xml') #TODO: Fix this!
        with open(file_path, encoding="utf-8") as f:
            article = f.read()
        tree = html.fromstring(article)
        content = tree.xpath(r'//*[@id="mw-content-text"]//text()')
        return ''.join(content)

    def set_single_counts(self):
        single_counts = SingleCount.objects.all()
        self.single_counts = Counter({item.entry.simple: item.count for item in single_counts})
        SingleCount.objects.all().delete()

    def update_single_counts(self, content):
        content = ''.join(content)
        exclude = whitespace + digits + ascii_letters + punctuation
        single_chars = [i for i in content if i not in exclude]
        self.single_counts.update(Counter(single_chars))

    def set_multi_counts(self):
        multi_counts = MultiCount.objects.all()
        self.multi_counts = Counter({item.entry.simple: item.count for item in multi_counts})
        MultiCount.objects.all().delete()

    def update_multi_counts(self, content):
        results = self.segmenter.segment(content).split()
        self.multi_counts.update(Counter(results))

    def load_to_db(self, Model, counts):
        records = []
        for phrase, count in counts.items():
            if phrase in self.entries:
                records.append(Model(entry=self.entries[phrase], count=count))
        Model.objects.bulk_create(records)

    def handle(self, *args, **options):
        self.set_single_counts()
        self.set_multi_counts()

        # for file in files:  TODO: make this a loop for a directory of files...
        content = self.extract_text_from_html()
        self.update_single_counts(content)
        self.update_multi_counts(content)

        #Load
        self.load_to_db(SingleCount, self.single_counts)
        self.load_to_db(MultiCount, self.multi_counts)