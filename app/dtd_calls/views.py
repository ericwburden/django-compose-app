import logging

from .forms import CallForm
from .models import Call

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy


class CallCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
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


class CallDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Call
    template_name = "dtd_calls/detail_call.html"


class CallListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Call
    template_name = "dtd_calls/list_call.html"
    paginate_by = 25