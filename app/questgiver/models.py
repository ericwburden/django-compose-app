import datetime
import logging

from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from uuid import uuid4


REPOST_PRIORITY_MULTIPLIER = 0.75


def uuid_str():
    return str(uuid4())


class Quest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    contact_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")], max_length=17
    )
    topic = models.CharField(max_length=200)
    description = models.TextField()
    days_allowed = models.IntegerField(default=7)
    priority = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    accepted = models.BooleanField(default=False)
    accepted_by_email = models.EmailField(max_length=200, blank=True, null=True)
    accepted_by_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
        max_length=17,
        blank=True,
        null=True,
    )
    accepted_at = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    retired = models.BooleanField(default=False)
    retired_at = models.DateTimeField(blank=True, null=True)
    abandoned = models.BooleanField(default=False)
    abandoned_at = models.DateTimeField(blank=True, null=True)
    reposted = models.BooleanField(default=False)
    reposted_at = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quest_approved_by",
    )
    status = models.CharField(max_length=15, blank=True, null=True)
    email_code = models.CharField(default=uuid_str, max_length=36)

    def __str__(self):
        return f"{self.created_at} - {self.topic} - {self.status}"

    def save(self, *args, **kwargs):
        if self.accepted and not self.accepted_at:
            self.accepted_at = timezone.now()
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        if self.retired and not self.retired_at:
            self.retired_at = timezone.now()
        if self.abandoned and not self.abandoned_at:
            self.abandoned_at = timezone.now()
        if self.approved and not self.approved_at:
            self.approved_at = timezone.now()
        if self.reposted and not self.reposted_at:
            self.reposted_at = timezone.now()
        self.status = "Submitted"
        if self.approved:
            self.status = "Approved"
        if self.reposted:
            self.status = "Reposted"
        if self.accepted:
            self.status = "Accepted"
        if self.retired:
            self.status = "Retired"
        if self.completed:
            self.status = "Completed"
        super().save(*args, **kwargs)

    def is_overdue(self):
        now = timezone.now()
        if self.accepted_at:
            return self.accepted_at + datetime.timedelta(days=self.days_allowed) < now
        return False

    def days_overdue(self):
        now = timezone.now()
        if self.is_overdue():
            td = now - (self.accepted_at + datetime.timedelta(days=self.days_allowed))
            return divmod(int(td.total_seconds()), 24 * 60 * 60)[0]
        return 0

    def sort_order(self):
        priority_multiplier = 1 / self.priority

        if self.reposted:
            days_since_update = timezone.now() - self.reposted_at
            return days_since_update * priority_multiplier * REPOST_PRIORITY_MULTIPLIER

        days_since_post = timezone.now() - self.created_at
        return days_since_post * priority_multiplier
