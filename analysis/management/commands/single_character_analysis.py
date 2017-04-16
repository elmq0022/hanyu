from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = '''
    parse a list of wikipedia xml articles and bag the occurence of 
    single characters.  
    '''

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        with open(r'./resources/wiki_zh_china.xml') as f:
            article = f.readline()
            print(article[:10])

