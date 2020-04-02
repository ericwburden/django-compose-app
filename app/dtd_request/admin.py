import pytz
from django.contrib import admin
from django.utils import timezone
from .models import Request, Response


class RequestAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "contact", "primary_phone", "type_of_need", "status")


class ResponseAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("request", "status", "created_at", "created_by")


admin.site.register(Request, RequestAdmin)
admin.site.register(Response, ResponseAdmin)
