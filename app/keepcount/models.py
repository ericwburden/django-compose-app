import uuid
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def uuid4_str():
    return str(uuid.uuid4())


# Create your models here.
class RegistrationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=36, default=uuid4_str)
    created = models.DateTimeField(auto_now=True)
    expires_after = models.DurationField(default=timedelta(days=5))

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            RegistrationCode.objects.create(user=instance)

    def is_expired(self):
        expiration_date = self.created + self.expires_after
        return expiration_date < timezone.now()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Counter(models.Model):
    counter_name = models.CharField(
        max_length=256,
        verbose_name="name",
        validators=[
            RegexValidator(
                r"^[a-zA-Z0-9_-]*$",
                message="Name must contain only letters, numbers, underscores, or dashes (no spaces).",
            )
        ],
        unique=True,
    )
    max_value = models.IntegerField(verbose_name="Maximum counter value")
    value = models.IntegerField(verbose_name="Current counter value", default=0)
    total = models.IntegerField(verbose_name="Total", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def warning_threshold(self):
        return self.max_value * 0.9

    def increment(self):
        Counter.objects.filter(counter_name=self.counter_name).update(
            value=F("value") + 1
        )
        Counter.objects.filter(counter_name=self.counter_name).update(
            total=F("total") + 1
        )
        history = CounterHistory(
            counter=self, operation=1, value=self.value + 1, total=self.total + 1
        )
        history.save()
        self.refresh_from_db()
        return self

    def decrement(self):
        if self.value > 0:
            Counter.objects.filter(counter_name=self.counter_name).update(
                value=F("value") - 1
            )
            history = CounterHistory(
                counter=self, operation=-1, value=self.value - 1, total=self.total
            )
            history.save()
            self.refresh_from_db()
        return self


class CounterHistory(models.Model):
    class Operation(models.IntegerChoices):
        SUBTRACT = -1
        ADD = 1

    counter = models.ForeignKey(
        Counter, on_delete=models.CASCADE, related_name="history"
    )
    recorded = models.DateTimeField(auto_now_add=True)
    operation = models.IntegerField(choices=Operation.choices)
    value = models.IntegerField(verbose_name="Current counter value", default=0)
    total = models.IntegerField(verbose_name="Total", default=0)
