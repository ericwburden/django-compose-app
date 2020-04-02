from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


review_choices = (
    ('RECEIVE', 'Received'),
    ('REVIEW', 'Under Review'),
    ('CONTACT', 'Contact Pending'),
    ('REFER', 'Referred'),
    ('CLOSE', 'Closed')
)


class DomainAssessment(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    score = models.IntegerField()
    description = models.TextField()


class Domain(models.Model):
    value = models.IntegerField(unique=True)
    label = models.CharField(max_length=100)


class Request(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")], max_length=17
    )
    home_phone = models.CharField(
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")], max_length=17
    )
    type_of_need = models.ForeignKey(Domain, on_delete=models.CASCADE)
    domain_score = models.IntegerField()
    add_info = models.TextField()


class Response(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="event_created_by",
    )
    status = models.CharField(max_length=4, choices=review_choices)