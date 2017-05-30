from django.db import models
from django.urls import reverse_lazy


class Entry(models.Model):
    traditional = models.CharField(max_length=255)
    simple = models.CharField(max_length=255)
    pin_yin = models.CharField(max_length=255)
    definitions = models.TextField()

    def __str__(self):
        return '{0}: {1}'.format(self.simple, self.pin_yin)

    def get_absolute_url(self):
        return reverse_lazy('dictionary:entry', kwargs={'pk': self.pk}) 