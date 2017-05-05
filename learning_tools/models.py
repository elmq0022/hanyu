from django.contrib.auth.admin import User
from django.db import models

from dictionary.models import Entry


class WordLearningStatus(models.Model):
    UNLEARNED = 'UN'
    ACQUIRING = 'AC'
    LEARNED = 'LN'
    LEARNING_STATUS = (
        (UNLEARNED, 'unlearned'),
        (ACQUIRING, 'acquiring'),
        (LEARNED, 'learned'),
    )
    entry = models.ForeignKey(Entry)
    user = models.ForeignKey(User)
    learning_status = models.CharField(max_length=2,
                                       choices=LEARNING_STATUS,
                                       default=UNLEARNED,
                                      )

    def __str__(self):
        return '{}: {}'.format(self.entry.simple, self.learning_status)

    class Meta:
        unique_together = (('entry', 'user'),)
