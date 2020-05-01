from django.contrib import admin
from .models import Counter

class CounterAdmin(admin.ModelAdmin):
    list_display = ("counter_name", "created_at", "value", "max_value", "total")

admin.site.register(Counter, CounterAdmin)