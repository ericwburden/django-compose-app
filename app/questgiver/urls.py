from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = "questgiver"

urlpatterns = [
    # Unauthenticated Pages ------------------------------------------------------------
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("request/", views.request_new, name="request"),
    # Authenticated Pages --------------------------------------------------------------
    path("pending/", views.PendingView.as_view(), name="pending"),
    path("<int:pk>/review/", views.ReviewView.as_view(), name="review"),
    path("<int:pk>/adjust/", views.AdjustView.as_view(), name="adjust"),
    path("overdue/", views.OverdueView.as_view(), name="overdue"),
    path("abandoned/", views.AbandonedView.as_view(), name="abandoned"),
    path("completed/", views.CompletedView.as_view(), name="completed"),
    path(
        "overdue/<int:pk>/review/",
        views.ReviewOverdueView.as_view(),
        name="review_overdue",
    ),
    # Unauthenticated Redirects --------------------------------------------------------
    path("request/submit/", views.submit_request, name="submit_request"),
    path("<int:quest_id>/accept/", views.accept_opportunity, name="accept"),
    path(
        "<int:pk>/complete/<str:code>",
        views.email_complete_response,
        name="email_complete",
    ),
    path(
        "<int:pk>/abandon/<str:code>",
        views.email_abandon_response,
        name="email_abandon",
    ),
    # Authenticated Redirects ----------------------------------------------------------
    path("<int:pk>/approve/submit/", views.approve_request, name="approve"),
    path("<int:pk>/adjust/submit/", views.submit_adjustment, name="submit_adjust"),
    path("<int:pk>/retire/submit/", views.retire_request, name="retire"),
    path("<int:pk>/repost/submit/", views.repost_request, name="repost"),
    # Utilities ------------------------------------------------------------------------
    path("message/<str:message>", views.message, name="message"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="questgiver:index"), name='logout'),
]
