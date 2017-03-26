from django.db import models


class Entry(models.Model):
    simple = models.CharField(max_length=100)
    traditional = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return '{0}: {1}'.format(self.simple, self.pronunciation)


class Definition(models.Model):
    entry = models.ForeignKey(Entry)
    order = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return '{0} for {1}'.format(str(self.order), str(self.entry))
