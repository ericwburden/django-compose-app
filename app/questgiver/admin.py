import pytz

from django.contrib import admin
from django.utils import timezone
from .models import Quest


class QuestAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "topic", "status")


admin.site.register(Quest, QuestAdmin)
