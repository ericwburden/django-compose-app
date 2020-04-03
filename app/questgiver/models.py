import datetime
import logging

from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from enum import Enum
from uuid import uuid4


REPOST_PRIORITY_MULTIPLIER = 0.75


def uuid_str():
    return str(uuid4())


class EventType(Enum):
    ERROR = "Error"
    SUBMIT = "Submitted"
    ADJUST = "Adjusted"
    REJECT = "Rejected"
    APPROVE = "Approved"
    ACCEPT = "Accepted"
    ABANDON = "Abandoned"
    COMPLETE = "Completed"
    REPOST = "Reposted"
    CLOSE = "Closed"


class Quest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    contact_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")], max_length=17
    )
    accepted_by_email = models.EmailField(max_length=200)
    accepted_by_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")], max_length=17
    )
    topic = models.CharField(max_length=200)
    description = models.TextField()
    days_allowed = models.IntegerField(default=7)
    priority = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    email_code = models.CharField(default=uuid_str, max_length=36)

    def save(self, event=None, *args, **kwargs):
        super(Quest, self).save(*args, **kwargs)
        if not event:
            event = Event(quest=self, event_type=EventType.SUBMIT.name)
        event.save()

    def __str__(self):
        return f"{self.topic} - {self.contact_name} ({self.id})"

    def last_event(self):
        return Event.objects.filter(quest=self.id).order_by("-created_at").first()

    def status(self):
        return self.last_event().event_type if self.last_event() else "ERROR"

    def status_label(self):
        return EventType[self.status()].value

    def last_update(self):
        return self.last_event().created_at if self.last_event() else None

    def last_event_of_type(self, event_type: EventType):
        return (
            Event.objects.filter(quest=self.id, event_type=event_type.name)
            .order_by("-created_at")
            .first()
        )

    def is_overdue(self):
        now = timezone.now()
        last_accepted = self.last_event_of_type(EventType.ACCEPT)
        if last_accepted:
            return (
                last_accepted.created_at + datetime.timedelta(days=self.days_allowed)
                < now
            )
        return False

    def days_overdue(self):
        now = timezone.now()
        if self.is_overdue():
            last_accepted = self.last_event_of_type(EventType.ACCEPT)
            td = now - (
                last_accepted.created_at + datetime.timedelta(days=self.days_allowed)
            )
            return divmod(int(td.total_seconds()), 24 * 60 * 60)[0]
        return 0

    def sort_order(self):
        priority_multiplier = 1 / self.priority

        last_reposted = self.last_event_of_type(EventType.REPOST)
        if last_reposted:
            days_since_update = timezone.now() - last_reposted.created_at
            return days_since_update * priority_multiplier * REPOST_PRIORITY_MULTIPLIER

        last_accepted = self.last_event_of_type(EventType.ACCEPT)
        if last_accepted:
            days_since_post = timezone.now() - last_accepted.created_at
            return days_since_post * priority_multiplier
        return 0


class Event(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    event_type = models.CharField(
        max_length=8, choices=[(tag.name, tag.value) for tag in EventType]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="event_created_by",
    )
