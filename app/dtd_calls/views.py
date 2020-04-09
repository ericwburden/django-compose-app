import logging

from .forms import CallForm, UpdateCallForm
from .models import Call

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count, Sum, DurationField, ExpressionWrapper, F
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone


class CallCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = Call
    template_name = "dtd_calls/create_call.html"
    form_class = CallForm

    def form_valid(self, form):
        logging.error("Checking Validation")
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.operator = self.request.user
            self.object.save()
        return HttpResponseRedirect(
            reverse_lazy("dtd_calls:call_detail", kwargs={"pk": self.object.id})
        )


class CallUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Call
    template_name = "dtd_calls/update-call.html"
    form_class = UpdateCallForm
    success_url = reverse_lazy("dtd_calls:call_list")


class CallDetailView(LoginRequiredMixin, DetailView):
    login_url = "/login/"
    model = Call
    template_name = "dtd_calls/detail_call.html"


class CallListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = Call
    template_name = "dtd_calls/list_call.html"
    paginate_by = 25
    ordering = ["-created_at"]


class CallTypeReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_calls/call-type-report.html"


def call_type_chart_data(request):
    labels = []
    incoming_calls = []
    outgoing_calls = []

    start_date = timezone.now() - timedelta(days=15)
    queryset = (
        Call.objects.filter(created_at__gt=start_date)
        .annotate(date=TruncDate("created_at"))
        .values("call_type", "date")
        .annotate(total_calls=Count("date"))
    )
    for entry in queryset:
        date_string = entry["date"].strftime("%m/%d/%Y")
        if date_string not in labels:
            labels.append(date_string)
        if entry["call_type"] == "Incoming":
            incoming_calls.append(entry["total_calls"])
        else:
            outgoing_calls.append(entry["total_calls"])

    return JsonResponse(
        data={
            "labels": labels,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
        }
    )


class CallDurationReport(LoginRequiredMixin, TemplateView):
    template_name = "dtd_calls/call-duration-report.html"


def call_duration_chart_data(request):
    labels = []
    incoming_calls = []
    outgoing_calls = []

    start_date = timezone.now() - timedelta(days=15)
    queryset = (
        Call.objects.filter(created_at__gt=start_date)
        .annotate(
            date=TruncDate("created_at"),
            duration=ExpressionWrapper(
                F("ended_at") - F("started_at"), output_field=DurationField()
            ),
        )
        .values("call_type", "date")
        .annotate(total_duration=Sum('duration'))
    )
    for entry in queryset:
        date_string = entry["date"].strftime("%m/%d/%Y")
        minutes = round(entry['total_duration'].seconds//60)
        print(entry['total_duration'])
        print(minutes)
        if date_string not in labels:
            labels.append(date_string)
        if entry["call_type"] == "Incoming":
            incoming_calls.append(minutes)
        else:
            outgoing_calls.append(minutes)

    return JsonResponse(
        data={
            "labels": labels,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
        }
    )
