import pytz

from django.contrib import admin
from django.utils import timezone
from .models import Quest, Event, EventType


class QuestAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "topic", "status_label", "last_update")


class EventAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("quest", "event_type", "created_at")
    list_filter = ('event_type', )


admin.site.register(Quest, QuestAdmin)
admin.site.register(Event, EventAdmin)
