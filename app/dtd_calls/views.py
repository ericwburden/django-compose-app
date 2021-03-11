import logging

from .forms import CallForm, UpdateCallForm, CallDomainFormset, CallStatusFormset
from .models import Call, Agency, CallStatus

from datetime import datetime, timedelta

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

    def get_context_data(self, **kwargs):
        data = super(CallCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["domains"] = CallDomainFormset(self.request.POST)
        else:
            data["domains"] = CallDomainFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        domains = context["domains"]
        other_agency = self.request.POST["other-agency"]
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.operator = self.request.user
            if other_agency:
                new_agency = Agency(name=other_agency)
                new_agency.save()
                self.object.referred_agency = new_agency
            self.object.save()
            if domains.is_valid():
                domains.instance = self.object
                domains.save()
            CallStatus(call=self.object, status=1, updated_by=self.request.user).save()
        return HttpResponseRedirect(
            reverse_lazy("dtd_calls:call_detail", kwargs={"pk": self.object.id})
        )


class CallUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Call
    template_name = "dtd_calls/update_call.html"
    form_class = UpdateCallForm
    success_url = reverse_lazy("dtd_calls:call_list")

    def get_context_data(self, **kwargs):
        data = super(CallUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["status"] = CallStatusFormset(self.request.POST)
        else:
            data["status"] = CallStatusFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        status_form = context["status"]
        other_agency = self.request.POST["other-agency"]
        with transaction.atomic():
            self.object = form.save(commit=False)
            if other_agency:
                new_agency = Agency(name=other_agency)
                new_agency.save()
                self.object.referred_agency = new_agency
            self.object.save()
            if status_form.is_valid():
                status_form.instance = self.object
                print(status_form.cleaned_data)
                status = status_form.cleaned_data[0]["status"]
                new_status = CallStatus(
                    call=self.object, status=status, updated_by=self.request.user
                )
                new_status.save()
        return HttpResponseRedirect(
            reverse_lazy("dtd_calls:call_detail", kwargs={"pk": self.object.id})
        )


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

def pulse(request):
    now = datetime.now()
    html = f"<html><body>{now}</body></html>"
    return HttpResponse(html)
