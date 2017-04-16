import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from lxml import html


class Command(BaseCommand):
    help = '''
    parse a list of wikipedia xml articles and bag the occurence of 
    single characters.  
    '''

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__()

    def handle(self, *args, **options):
        with open(os.path.join(self.base_dir, 'resources', 'wiki_zh_china.xml'), encoding="utf-8") as f:
            article = f.read()
            tree = html.fromstring(article)
            # content = tree.xpath(r'//*[@id="mw-content-text"]/*/text()')
            # content = tree.xpath(r'//*[@id="mw-content-text"]/p/text()|//*[@id="mw-content-text"]/p/*/text()')
            # content = tree.xpath(r'//*[@id="mw-content-text"]/p/descendant-or-self')
            content = tree.xpath(r'//*[@id="mw-content-text"]//text()')
            pprint(content[500:600])