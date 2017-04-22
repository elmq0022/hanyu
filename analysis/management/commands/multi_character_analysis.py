import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from lxml import html

from string import whitespace
from string import ascii_letters 
from string import digits
from string import punctuation

from collections import Counter
# import regex as re

from nltk.tokenize import stanford_segmenter

class Command(BaseCommand):
    help = '''
    parse a list of wikipedia xml articles and bag the occurence of 
    single characters.  
    '''

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__()


    def handle(self, *args, **options):
        '''
        Article is located at: https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD
        '''
        with open(os.path.join(self.base_dir, 'resources', 'wiki_zh_china.xml'), encoding="utf-8") as f:
            article = f.read()
        tree = html.fromstring(article)
        # content = tree.xpath(r'//*[@id="mw-content-text"]/*/text()')
        # content = tree.xpath(r'//*[@id="mw-content-text"]/p/text()|//*[@id="mw-content-text"]/p/*/text()')
        # content = tree.xpath(r'//*[@id="mw-content-text"]/p/descendant-or-self')
        content = tree.xpath(r'//*[@id="mw-content-text"]//text()')
        content = ''.join(content)
        STFD_SEG_DIR = os.path.join(self.base_dir,'stanford_segmenter_resources', 'stanford-segmenter-2016-10-31') 
        STFD_SEG = os.path.join(STFD_SEG_DIR, 'stanford-segmenter-3.7.0.jar')
        SLF4J = os.path.join(STFD_SEG_DIR, 'slf4j-api-1.7.25.jar')
        SIHAN_DICT = os.path.join(STFD_SEG_DIR, 'data')
        MODEL = os.path.join(STFD_SEG_DIR, 'data', 'pku.gz')
        DICT = os.path.join(STFD_SEG_DIR, 'data', 'dict-chris6.ser.gz')

        os.environ['JAVAHOME'] = r'C:\Program Files\Java\jre1.8.0_131\bin\java.exe'

        s = stanford_segmenter.StanfordSegmenter(
            path_to_jar=STFD_SEG,
            path_to_slf4j=SLF4J,
            path_to_sihan_corpora_dict=SIHAN_DICT,
            path_to_model=MODEL,
            path_to_dict=DICT
            )

        sentence = u"这是斯坦福中文分词器测试"
        pprint(s.segment(sentence))