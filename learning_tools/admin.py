from django.contrib import admin
from .models import WordLearningStatus


class WordLearningStatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(WordLearningStatus, WordLearningStatusAdmin)