from .views import (
    HomePageView,
    UserRegistrationFormView,
    RegistrationSubmittedView,
    NewCounterView,
    ExistingCounterView,
    ExistingCounterJsonView,
    AddToCounterView,
    SubtractFromCounterView,
)

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("new/", NewCounterView.as_view(), name="new_counter"),
    path(
        "counter/<str:counter_name>",
        ExistingCounterView.as_view(),
        name="existing_counter",
    ),
    path(
        "counter/<str:counter_name>/json",
        ExistingCounterJsonView.as_view(),
        name="existing_counter_json",
    ),
    path(
        "counter/<str:counter_name>/add",
        AddToCounterView.as_view(),
        name="add_to_counter",
    ),
    path(
        "counter/<str:counter_name>/subtract",
        SubtractFromCounterView.as_view(),
        name="subtract_from_counter",
    ),
    path("accounts/", include("allauth.urls")),  # <--
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/admin", admin.site.urls),
    path("register/", UserRegistrationFormView.as_view(), name="register"),
    path("registered/", RegistrationSubmittedView.as_view(), name="registered"),
]
