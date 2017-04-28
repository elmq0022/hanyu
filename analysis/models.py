from django.db import models
from dictionary.models import Entry


class Count(models.Model):
    WORD = 'w'
    CHARACTER = 'c'
    WORD_OR_CHARACTER = (
        (WORD, 'word'),
        (CHARACTER, 'character'),
    )
    entry = models.ForeignKey(Entry)
    count = models.IntegerField()
    count_type = models.CharField(max_length=2,
                                  choices=WORD_OR_CHARACTER,
                                  default='m',
                                 )

    def __str__(self):
        return '{}:{}:{}'.format(self.entry, self.count, self.count_type)