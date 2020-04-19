import pytz
from django.contrib import admin
from django.utils import timezone
from .models import Call, Agency, Domain, CallStatus


class CallStatusInline(admin.StackedInline):
    model = CallStatus
    extra = 0


class DomainInline(admin.StackedInline):
    model = Domain
    extra = 0


class CallAdmin(admin.ModelAdmin):
    timezone.activate(pytz.timezone("America/Chicago"))
    list_display = ("created_at", "caller_number", "caller_zip", "duration")
    inlines = [DomainInline, CallStatusInline]


class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Call, CallAdmin)
admin.site.register(Agency, AgencyAdmin)
