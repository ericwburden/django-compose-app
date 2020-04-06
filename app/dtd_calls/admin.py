import pytz
from django.contrib import admin
from django.utils import timezone
from .models import Call



class CallAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "caller_number", "caller_zip", "duration")


admin.site.register(Call, CallAdmin)