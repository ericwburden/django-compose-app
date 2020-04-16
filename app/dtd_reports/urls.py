from . import views
from django.urls import path

app_name = "dtd_reports"

urlpatterns = [
    # Template View URLs ---------------------------------------------------------------
    path(
        "call-duration",
        views.CallDurationReport.as_view(),
        name="call-duration-report",
    ),
    path("call-type", views.CallTypeReport.as_view(), name="call-type-report"),
    path(
        "call-referral",
        views.CallReferralReport.as_view(),
        name="call-referral-report",
    ),
    path(
        "request-domain",
        views.RequestDomainReport.as_view(),
        name="request-domain-report",
    ),
    path(
        "total-calls-requests",
        views.TotalCallsRequestsReport.as_view(),
        name="total-calls-requests-report",
    ),
    # Data View URLs -------------------------------------------------------------------
    path("call-type/data", views.call_type_report_data, name="call-type-report-data",),
    path(
        "call-duration/data",
        views.call_duration_report_data,
        name="call-duration-report-data",
    ),
    path(
        "call-referral/data",
        views.call_referral_report_data,
        name="call-referral-report-data",
    ),
    path(
        "request-domain/data",
        views.request_domain_report_data,
        name="request-domain-report-data",
    ),
    path(
        "total-calls-requests/data",
        views.total_calls_requests_report_data,
        name="total-calls-requests-report-data",
    ),
]
