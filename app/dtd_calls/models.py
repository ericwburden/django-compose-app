from dtd_request.models import domains

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Agency(models.Model):
    class Meta:
        verbose_name_plural = "Agencies"
        ordering = ["-pk"]

    name = models.CharField(verbose_name="Agency Name", max_length=256)

    def __str__(self):
        return self.name


class Call(models.Model):
    INCOMING = "Incoming"
    OUTGOING = "Outgoing"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(verbose_name="Call Started")
    ended_at = models.DateTimeField(verbose_name="Call Ended")
    caller_name = models.CharField(verbose_name="Caller Name", max_length=256, null=True)
    caller_address = models.CharField(verbose_name="Caller Street Address", max_length=256, null=True)
    caller_city = models.CharField(verbose_name="Caller City", max_length=256, null=True)
    caller_state = models.CharField(verbose_name="Caller State (2-Letter)", max_length=2, help_text="TN", null=True)
    caller_zip = models.CharField(
        validators=[RegexValidator(r"^\d{5}$")],
        max_length=5,
        verbose_name="Caller Zip Code",
        help_text="#####",
    )
    caller_number = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{3}-?\d{3}-?\d{4}$")],
        max_length=17,
        verbose_name="Caller Phone Number",
        help_text="###-###-####",
    )
    caller_email = models.EmailField(verbose_name="Caller Email Address", null=True)
    caller_age = models.IntegerField(verbose_name="Caller Age", null=True)
    caller_gender = models.CharField(verbose_name="Caller Gender", choices = (("M", "Male"), ("F", "Female"), ("O", "Other")), max_length=1, null=True)
    caller_household_size = models.IntegerField(verbose_name="Caller Household Size", null=True)
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
    referred_agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    followup_notes  = models.TextField(verbose_name="Followup Notes", blank=True, null=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="call_operator",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="call_assigned_to",
    )

    def duration(self):
        diff = self.ended_at - self.started_at
        minutes = divmod(diff.seconds, 60)
        return f"{minutes[0]} minutes, {minutes[1]} seconds"

    def status(self):
        return Call.objects.get(pk=self.id).statuses.latest('id')


class Domain(models.Model):
    call = models.ForeignKey(Call, related_name="domains", on_delete=models.CASCADE)
    domain = models.IntegerField(choices=domains, verbose_name="Service Domain(s)")

    def __str__(self):
        return next(i[-1] for i in domains if i[0] == self.domain)

    def label(self):
        return self.__str__()


class CallStatus(models.Model):
    class Meta:
        ordering = ["-created_at"]
        
    CONTACTED = "Contacted"
    REFERRED = "Referred"
    INFO = "Shared Information"
    CLOSED = "Closed"
    statuses = ((1, CONTACTED), (2, REFERRED), (3, INFO), (4, CLOSED))

    created_at = models.DateTimeField(auto_now_add=True)
    call = models.ForeignKey(Call, related_name="statuses", on_delete=models.CASCADE)
    status = models.IntegerField(choices = statuses, verbose_name="Call Status")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="status_updated_by",
    )

    def __str__(self):
        return next(i[-1] for i in self.statuses if i[0] == self.status)

    def label(self):
        return self.__str__()
