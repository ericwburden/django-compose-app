from django.contrib import admin
from .models import Counter, CounterPosition


class CounterPositionAdmin(admin.StackedInline):
    model = CounterPosition


class CounterAdmin(admin.ModelAdmin):
    list_display = ("counter_name", "created_at", "value", "max_value", "total")
    inlines = (CounterPositionAdmin, )


admin.site.register(Counter, CounterAdmin)
