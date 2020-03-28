import logging

from .mail import acceptance_email, completed_email, accepted_email
from .models import Quest

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse


# Unauthenticated Pages ----------------------------------------------------------------


class IndexView(generic.ListView):
    template_name = "questgiver/index.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        open_quests = Quest.objects.filter(
            approved=True, accepted=False, retired=False
        ).all()
        return sorted(open_quests, key=lambda x: x.sort_order())


class DetailView(generic.DetailView):
    model = Quest
    template_name = "questgiver/detail.html"

    def get_queryset(self):
        """
        Excludes any quests that aren't approved, or quests that are currently
        accepted or retired
        """
        open_quests = Quest.objects.filter(approved=True, accepted=False, retired=False)
        return open_quests


def request_new(request):
    return render(request, "questgiver/request.html")


# Authenticated Pages ------------------------------------------------------------------


class PendingView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/pending.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        return Quest.objects.filter(approved=False, retired=False).order_by(
            "-created_at"
        )


class ReviewView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/review.html"

    def get_queryset(self):
        """
        Excludes any quests that are approved or retired
        """
        return Quest.objects.filter(approved=False, retired=False)


class ReviewOverdueView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/review.html"

    def get_queryset(self):
        return Quest.objects.filter(reposted=False, retired=False)
        return [q for q in quests if q.is_overdue()]


class AdjustView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/adjust.html"

    def get_queryset(self):
        """
        Excludes any quests that aren't approved, or quests that are currently
        accepted or retired
        """
        return Quest.objects.filter(approved=False, retired=False)


class OverdueView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/overdue.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        quests = Quest.objects.filter(reposted=False, retired=False).all()
        return [q for q in quests if q.is_overdue()]


class AbandonedView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/abandoned.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        return Quest.objects.filter(abandoned=True, retired=False).all()


class CompletedView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/completed.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        return Quest.objects.filter(completed=True, retired=False).all()


# Unauthenticated Redirects ------------------------------------------------------------


def accept_opportunity(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    if quest.accepted:
        message = "already_accepted"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    quest.accepted = True
    quest.accepted_by_email = request.POST["email"]
    quest.accepted_by_phone = request.POST["phone"].replace("-", "")
    message = "accepted"
    if acceptance_email(quest):
        try:
            quest.save()
        except Exception as exc:
            logging.error(exc)
            message = "error"
    else:
        message = "email_error"
    accepted_email(quest)
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def submit_request(request):
    quest = Quest(
        contact_name=request.POST["contact_name"],
        contact_email=request.POST["contact_email"],
        contact_phone=request.POST["contact_phone"],
        topic=request.POST["topic"],
        description=request.POST["description"],
        days_allowed=request.POST["days_allowed"],
        priority=request.POST["priority"],
    )
    message = "submitted"
    try:
        quest.save()
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def email_complete_response(request, pk, code):
    quest = get_object_or_404(Quest, pk=pk)
    message = "unverified"
    if quest.completed:
        message = "already_completed"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    if quest.email_code == code:
        quest.completed = True
        message = "completed"
        try:
            quest.save()
        except Exception as exc:
            logging.error(exc)
            message = "error"
        completed_email(quest)
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def email_abandon_response(request, pk, code):
    quest = get_object_or_404(Quest, pk=pk)
    message = "unverified"
    if quest.completed:
        message = "already_completed"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    if quest.email_code == code:
        quest.abandoned = True
        message = "abandoned"
        try:
            quest.save()
        except Exception as exc:
            logging.error(exc)
            message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


# Authenticated Redirects --------------------------------------------------------------


def approve_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.accepted:
        message = "already_approved"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    quest.approved = True
    message = "approved"
    try:
        quest.save()
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def retire_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.retired:
        message = "already_retired"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    quest.retired = True
    message = "retired"
    try:
        quest.save()
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def submit_adjustment(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    quest.contact_name = request.POST["contact_name"]
    quest.contact_email = request.POST["contact_email"]
    quest.contact_phone = request.POST["contact_phone"]
    quest.topic = request.POST["topic"]
    quest.description = request.POST["description"]
    quest.days_allowed = request.POST["days_allowed"]
    quest.priority = request.POST["priority"]
    message = "adjusted"
    try:
        quest.save()
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def repost_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.reposted:
        message = "already_reposted"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    reposted_quest = Quest(
        id=quest.id,
        created_at=quest.created_at,
        updated_at=quest.updated_at,
        reposted=True,
        contact_name=quest.contact_name,
        contact_email=quest.contact_email,
        contact_phone=quest.contact_phone,
        topic=quest.topic,
        description=quest.description,
        days_allowed=quest.days_allowed,
        priority=quest.priority,
        approved=quest.approved,
        approved_at=quest.approved_at,
    )
    message = "reposted"
    try:
        reposted_quest.save()
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


# Utilities ----------------------------------------------------------------------------


def message(request, message):
    return render(request, "questgiver/message.html", {"message": message})
