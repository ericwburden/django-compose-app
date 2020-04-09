from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = "dtd_calls"

urlpatterns = [
    path("", views.CallCreateView.as_view(), name="call_create"),
    path("<int:pk>/", views.CallDetailView.as_view(), name="call_detail"),
    path("update/<int:pk>/", views.CallUpdateView.as_view(), name="call_update"),
    path("all/", views.CallListView.as_view(), name="call_list"),
    path("report/call-type/", views.CallTypeReport.as_view(), name="call-type-report"),
    path(
        "report/call-duration/",
        views.CallDurationReport.as_view(),
        name="call-duration-report",
    ),
]
