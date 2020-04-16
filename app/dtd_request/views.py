import logging

from .forms import (
    RequestForm,
    MyRequestSearchForm,
    RequestDomainFormset,
    LinkReferralForm,
    UpdateStatusForm,
)
from .models import Request, Response
from dtd_emails.tasks import status_update_email

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Q, Max
from django.forms import TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse


class RequestView(CreateView):
    model = Request
    template_name = "dtd_request/request.html"
    form_class = RequestForm

    def get_context_data(self, **kwargs):
        data = super(RequestView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["domains"] = RequestDomainFormset(self.request.POST)
        else:
            data["domains"] = RequestDomainFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        domains = context["domains"]
        with transaction.atomic():
            self.object = form.save()
            if domains.is_valid():
                domains.instance = self.object
                domains.save()
        code = form.cleaned_data["confirmation_code"]
        return HttpResponseRedirect(
            reverse_lazy("dtd_request:thanks", kwargs={"code": code})
        )


class ThanksMsgView(TemplateView):
    template_name = "dtd_request/thanks.html"


class MyRequestSearch(FormView):
    template_name = "dtd_request/my-request-search.html"
    form_class = MyRequestSearchForm

    def form_valid(self, form):
        phone = form.cleaned_data["primary_phone"]
        code = form.cleaned_data["confirmation_code"]
        return HttpResponseRedirect(
            reverse_lazy(
                "dtd_request:my_request", kwargs={"phone": phone, "code": code}
            )
        )


class MyRequest(DetailView):
    model = Request
    template_name = "dtd_request/my-request.html"

    def get_object(self):
        try:
            return Request.objects.get(
                primary_phone=self.kwargs["phone"],
                confirmation_code=self.kwargs["code"],
            )
        except ObjectDoesNotExist:
            return None


class ManageRequests(LoginRequiredMixin, ListView):
    login_url = "/login/"
    template_name = "dtd_request/manage-requests.html"
    context_object_name = "requests"
    paginate_by = 50

    def get_queryset(self):
        return (
            Request.objects.annotate(latest_response=Max("response__created_at"))
            .filter(
                Q(response__created_at=F("latest_response")),
                ~Q(response__status="CLOSED"),
            )
            .order_by("-response__created_at")
        )


class UpdateRequest(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = Response
    form_class = UpdateStatusForm
    template_name = "dtd_request/referral-note.html"
    success_url = "/manage/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = self.kwargs["status"]
        context["request"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        self.object = form.save()
        status_update_email.delay(self.object.id)
        return super(UpdateRequest, self).form_valid(form)


class LinkReferral(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Request
    form_class = LinkReferralForm
    template_name = "dtd_request/link_referral.html"

    def get_success_url(self):
        return reverse("dtd_request:update", args=[self.object.id, "REFERRED"])
