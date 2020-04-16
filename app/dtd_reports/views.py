import pytz

from dtd_calls.models import Call
from dtd_request.models import Domain, domains
from datetime import timedelta

from django.db.models import Count, ExpressionWrapper, DurationField, F, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone


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
