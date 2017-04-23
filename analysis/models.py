from django.db import models
from dictionary.models import Entry

class SingleCount(models.Model):
    entry = models.ForeignKey(Entry)
    count = models.IntegerField()

    def __str__(self):
        return '{entry}: {count}'.format(entry=self.entry, count=self.count)


class MultiCount(models.Model):
    entry = models.ForeignKey(Entry)
    count = models.IntegerField()

    def __str__(self):
        return '{entry}: {count}'.format(entry=self.entry, count=self.count)
