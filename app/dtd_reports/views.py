import pytz
import csv
import os

from dtd_calls.models import Call
from dtd_request.models import Request, Domain, domains
from .models import WeeklyReport
from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, ExpressionWrapper, DurationField, F, Sum, Max
from django.db.models.functions import TruncDate
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.utils import timezone

# =======================================================================================
# region Data Views --------------------------------------------------------------------
# =======================================================================================


def call_type_report_data(request):
    labels = []
    incoming_calls = []
    outgoing_calls = []
    tz = pytz.timezone("America/Chicago")

    start_date = timezone.now() - timedelta(days=15)
    queryset = (
        Call.objects.filter(created_at__gt=start_date)
        .annotate(date=TruncDate("created_at", tzinfo=tz))
        .values("call_type", "date")
        .annotate(total_calls=Count("date"))
        .order_by("date", "call_type")
    )

    for entry in queryset:
        date_string = entry["date"].strftime("%m/%d/%Y")
        if date_string not in labels:
            labels.append(date_string)
            if len(labels) > len(incoming_calls) + 1:
                incoming_calls.append(0)
            if len(labels) > len(outgoing_calls) + 1:
                outgoing_calls.append(0)

        if entry["call_type"] == "Incoming":
            incoming_calls.append(entry["total_calls"])
        elif entry["call_type"] == "Outgoing":
            outgoing_calls.append(entry["total_calls"])

    return JsonResponse(
        data={
            "labels": labels,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
        }
    )


def call_duration_report_data(request):
    labels = []
    incoming_calls = []
    outgoing_calls = []
    tz = pytz.timezone("America/Chicago")

    start_date = timezone.now() - timedelta(days=15)
    queryset = (
        Call.objects.filter(created_at__gt=start_date)
        .annotate(
            date=TruncDate("created_at", tzinfo=tz),
            duration=ExpressionWrapper(
                F("ended_at") - F("started_at"), output_field=DurationField()
            ),
        )
        .values("call_type", "date")
        .annotate(total_duration=Sum("duration"))
        .order_by("date", "call_type")
    )
    for entry in queryset:
        date_string = entry["date"].strftime("%m/%d/%Y")
        minutes = round(entry["total_duration"].seconds // 60)

        if date_string not in labels:
            labels.append(date_string)
            if len(labels) > len(incoming_calls) + 1:
                incoming_calls.append(0)
            if len(labels) > len(outgoing_calls) + 1:
                outgoing_calls.append(0)

        if entry["call_type"] == "Incoming":
            incoming_calls.append(minutes)
        elif entry["call_type"] == "Outgoing":
            outgoing_calls.append(minutes)

    return JsonResponse(
        data={
            "labels": labels,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
        }
    )


def call_referral_report_data(request):
    queryset = Call.objects.values("client_referred").annotate(
        n=Count("client_referred")
    )
    call_count = Call.objects.count()

    labels = [
        "Referred" if entry["client_referred"] else "Not Referred" for entry in queryset
    ]
    percents = [round((entry["n"] / call_count) * 100) for entry in queryset]

    return JsonResponse(data={"labels": labels, "percents": percents})


def request_domain_report_data(request):
    queryset = (
        Domain.objects.values("domain").annotate(n=Count("domain")).order_by("-n")[:5]
    )

    def to_label(domain: int):
        return next(i[-1] for i in domains if i[0] == domain)

    labels = [to_label(entry["domain"]) for entry in queryset]
    counts = [entry["n"] for entry in queryset]

    return JsonResponse(data={"labels": labels, "counts": counts})


def total_calls_requests_report_data(request):
    incoming_calls = Call.objects.filter(call_type="Incoming").count()
    online_intakes = Request.objects.count()

    labels = ["Incoming Calls", "Online Intakes"]
    counts = [incoming_calls, online_intakes]

    return JsonResponse(data={"labels": labels, "counts": counts})


def weekly_report_data(request):
    current_week_records = WeeklyReport.objects.annotate(current_week=Max('week_start')).filter(week_start=F('current_week'))
    return JsonResponse(data={'reports': [model_to_dict(i) for i in current_week_records]})


def weekly_report_csv(request):
    weekly_report_records = WeeklyReport.objects.order_by('week_start').all()
    file_name = f"Weekly Call Center Report as of {datetime.now().date()}.csv"

    if not os.path.exists(os.path.join(settings.BASE_DIR, 'data')):
        os.makedirs(os.path.join(settings.BASE_DIR, 'data'))

    file_path = os.path.join(settings.BASE_DIR, f'data/{file_name}')
    with open(file_path, 'w') as output_file:
        writer = csv.writer(output_file, delimiter=',') 
        headers = ['Week Start', 'Domain', 'Calls', 'Calls Referred', 'Online Requests', 'Online Requests Referred']  
        writer.writerow(headers)
        for w in weekly_report_records:
            row = [w.week_start, w.domain, w.calls, w.calls_referred, w.requests, w.requests_referred]
            writer.writerow(row)

    with open(file_path,'r') as csv_file:
        resp = HttpResponse(csv_file.read(), content_type='application/x-download')
        resp['Content-Disposition'] = f'attachment;filename={file_name}'
    return resp


# =======================================================================================
# endregion ----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# region Template Views ----------------------------------------------------------------
# =======================================================================================


class CallTypeReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_reports/call-type-report.html"


class CallDurationReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_reports/call-duration-report.html"


class CallReferralReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_reports/call-referral-report.html"


class RequestDomainReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_reports/request-domain-report.html"


class TotalCallsRequestsReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_reports/total-calls-requests-report.html"


class WeeklyReportView(LoginRequiredMixin, ListView):
    model = WeeklyReport
    paginate_by = 100
    template_name = "dtd_reports/weekly-report.html"


# =======================================================================================
# endregion ----------------------------------------------------------------------------
# =======================================================================================
