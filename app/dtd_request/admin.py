import pytz
from django.contrib import admin
from django.utils import timezone
from .models import Request, Response, Domain


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    ordering = ("-created_at",)


class DomainInline(admin.StackedInline):
    model = Domain
    extra = 0


class RequestAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "contact", "primary_phone", "status")
    inlines = [ResponseInline, DomainInline]


admin.site.register(Request, RequestAdmin)
