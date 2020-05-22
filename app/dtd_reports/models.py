from django.db import models


class WeeklyReport(models.Model):
    week_start = models.DateTimeField(verbose_name="First Day of Report Week")
    domain = models.CharField(max_length=200, verbose_name="TTS Domain")
    calls = models.IntegerField(verbose_name="Number of Calls")
    calls_referred = models.IntegerField(verbose_name="Number of Calls Referred")
    requests = models.IntegerField(verbose_name="Number of Online Requests")
    requests_referred = models.IntegerField(verbose_name="Number of Online Requests Referred")

    class Meta:
        managed = False
        db_table = "weekly_report"
