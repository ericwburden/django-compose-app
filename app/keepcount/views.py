from .models import Profile, Counter
from .forms import NewCounterForm, CounterNameSearch

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import F
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView


class HomePageView(FormView):
    template_name = "keepcount/home.html"
    form_class = CounterNameSearch

    def form_valid(self, form):
        self.counter_name = form.cleaned_data["counter_name"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("existing_counter", kwargs={"counter_name": self.counter_name})


class NewCounterView(CreateView):
    model = Counter
    template_name = "keepcount/new_counter.html"
    form_class = NewCounterForm

    def form_valid(self, form):
        self.counter_name = form.cleaned_data["counter_name"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("existing_counter", kwargs={"counter_name": self.counter_name})


class AddToCounterView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Counter.objects.filter(counter_name=kwargs["counter_name"]).update(value=F("value") + 1)
        return reverse_lazy("existing_counter", kwargs={"counter_name": kwargs["counter_name"]})


class SubtractFromCounterView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Counter.objects.filter(counter_name=kwargs["counter_name"], value__gt=0).update(value=F("value") - 1)
        return reverse_lazy("existing_counter", kwargs={"counter_name": kwargs["counter_name"]})


class ExistingCounterView(DetailView):
    model = Counter
    template_name = "keepcount/existing_counter.html"
    slug_field = "counter_name"
    slug_url_kwarg = "counter_name"


class ExistingCounterJsonView(DetailView):
    model = Counter
    slug_field = "counter_name"
    slug_url_kwarg = "counter_name"

    def render_to_response(self, context, **response_kwargs):
        dict_obj = model_to_dict(context["object"])
        return JsonResponse(dict_obj, **response_kwargs)


class UserRegistrationFormView(FormView):
    template_name = "registration/user_registration_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("registered")

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        print(user.registrationcode.code)
        return super().form_valid(form)


class RegistrationSubmittedView(TemplateView):
    template_name = "registration/registration_submitted.html"


class GoogleLogin(TemplateView):
    template_name = "social_app/index.html"