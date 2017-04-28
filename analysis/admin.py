from django.contrib import admin
from .models import Count


class CountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Count, CountAdmin)
