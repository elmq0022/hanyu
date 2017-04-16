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
            pprint(content[500:600])