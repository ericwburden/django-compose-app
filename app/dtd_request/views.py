import logging

from .forms import RequestForm, MyRequestSearchForm, RequestDomainFormset
from .models import Request, Response

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Q, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
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
    template_name = "dtd_request/manage-requests.html"
    context_object_name = "requests"

    def get_queryset(self):
        return (
            Request.objects.annotate(latest_response=Max("response__created_at"))
            .filter(
                Q(response__created_at=F("latest_response")),
                ~Q(response__status="CLOSED"),
            )
            .order_by("-response__created_at")
        )


class UpdateRequest(LoginRequiredMixin, RedirectView):
    pattern_name = "dtd_request:manage"

    def get_redirect_url(self, *args, **kwargs):
        request = get_object_or_404(Request, pk=self.kwargs["pk"])
        response = Response(
            request=request, status=self.kwargs["status"], created_by=self.request.user
        )
        response.save()
        # return super().get_redirect_url(*args, **kwargs)
        return reverse("dtd_request:manage")
