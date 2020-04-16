from . import views
from django.urls import path

app_name = "dtd_reports"

urlpatterns = [
    # Template View URLs ---------------------------------------------------------------
    path(
        "total-calls-requests/report",
        views.TotalCallsRequestsReport.as_view(),
        name="total-calls-requests-report",
    ),
    # Data View URLs -------------------------------------------------------------------
    path(
        "call-type-report", views.call_type_report_data, name="call-type-report-data",
    ),
    path(
        "call-duration-report",
        views.call_duration_report_data,
        name="call-duration-report-data",
    ),
    path(
        "call-referral-report",
        views.call_referral_report_data,
        name="call-referral-report-data",
    ),
    path(
        "request-domain-report",
        views.request_domain_report_data,
        name="request-domain-report-data",
    ),
    path(
        "total-calls-requests-report",
        views.total_calls_requests_report_data,
        name="total-calls-requests-report-data",
    ),
]
