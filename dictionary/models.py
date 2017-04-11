from django.db import models


class Entry(models.Model):
    traditional = models.CharField(max_length=255)
    simple = models.CharField(max_length=255)
    pin_yin = models.CharField(max_length=255)
    definitions = models.TextField()

    def __str__(self):
        return '{0}: {1}'.format(self.simple, self.pin_yin)