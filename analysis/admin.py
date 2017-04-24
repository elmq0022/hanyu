from django.contrib import admin
from .models import SingleCount, MultiCount


class SingleCountAdmin(admin.ModelAdmin):
    pass


class MultiCountAdmin(admin.ModelAdmin):
    pass


admin.site.register(SingleCount, SingleCountAdmin)
admin.site.register(MultiCount, MultiCountAdmin)
