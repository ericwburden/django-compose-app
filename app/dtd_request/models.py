from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from uuid import uuid4


review_choices = (
    ("PENDING", "Pending"),
    ("RECEIVED", "Received"),
    ("REVIEWED", "Under Review"),
    ("CONTACTED", "Contact Pending"),
    ("REFERRED", "Referred"),
    ("CLOSED", "Closed"),
)


def short_code():
    return str(uuid4())[:8]


class Domain(models.Model):
    value = models.IntegerField(unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact = models.CharField(
        max_length=200, verbose_name="Your Name", help_text="First Last"
    )
    email = models.EmailField(
        max_length=200, blank=True, null=True, verbose_name="Your Email Address"
    )
    primary_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Phone number where you can be reached",
        help_text="###-###-####",
    )
    secondary_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Backup phone number",
        help_text="###-###-####",
    )
    type_of_need = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        verbose_name="What kind of help are you looking for?",
        blank=False,
    )
    add_info = models.TextField(
        verbose_name="Please provide any additional information here",
        help_text="Share anything else you'd like for us to know",
    )
    confirmation_code = models.CharField(max_length=8, default=short_code)

    def __str__(self):
        return f'{self.contact}:{self.type_of_need} ({self.id})'

    def save(self, response=None, *args, **kwargs):
        super(Request, self).save(*args, **kwargs)
        if not response:
            response = Response(request=self, status="PENDING")
        response.save()

    def last_response(self):
        return Response.objects.filter(request=self.id).order_by("-created_at").first()

    def status(self):
        return self.last_response().status if self.last_response() else "PENDING"


class Response(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="response_created_by",
    )
    status = models.CharField(max_length=9, choices=review_choices)
