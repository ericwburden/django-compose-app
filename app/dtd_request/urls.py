from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = "dtd_request"

urlpatterns = [
    # Unauthenticated Pages ------------------------------------------------------------
    path("", views.RequestView.as_view(), name="request"),
    path("thanks/<str:code>", views.ThanksMsgView.as_view(), name="thanks"),
    path("search/", views.MyRequestSearch.as_view(), name="my_request_search"),
    path("status/<str:phone>/<str:code>", views.MyRequest.as_view(), name="my_request"),
    # Authenticated Pages --------------------------------------------------------------
    path("manage/", views.ManageRequests.as_view(), name="manage"),
    # Authenticated Redirects ----------------------------------------------------------
    path("update/<int:pk>/<str:status>", views.UpdateRequest.as_view(), name="update"),
    # Utilities ------------------------------------------------------------------------
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="dtd_request:request"),
        name="logout",
    ),
]
