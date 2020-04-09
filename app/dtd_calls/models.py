from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Call(models.Model):
    INCOMING = "Incoming"
    OUTGOING = "Outgoing"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(verbose_name="Call Started")
    ended_at = models.DateTimeField(verbose_name="Call Ended")
    caller_number = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{3}-?\d{3}-?\d{4}$")],
        max_length=17,
        verbose_name="Caller Phone Number",
        help_text="###-###-####",
    )
    caller_zip = models.CharField(
        validators=[RegexValidator(r"^\d{5}$")],
        max_length=5,
        verbose_name="Caller Zip Code",
        help_text="#####",
    )
    call_type = models.CharField(
        max_length=8,
        choices=((INCOMING, "Incoming"), (OUTGOING, "Outgoing")),
        default="Incoming",
        verbose_name="Type of Call",
    )
    covid_related = models.BooleanField(
        verbose_name="Is this call related to Covid-19?", default=False
    )
    client_referred = models.BooleanField(
        verbose_name="Was this client referred to a provider?", default=False
    )
    referral_id = models.IntegerField(verbose_name="Referral ID", blank=True, null=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="call_operator",
    )

    def duration(self):
        diff = self.ended_at - self.started_at
        minutes = divmod(diff.seconds, 60)
        return f"{minutes[0]} minutes, {minutes[1]} seconds"
