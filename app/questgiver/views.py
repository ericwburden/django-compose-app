import logging

from .mail import acceptance_email, completed_email, accepted_email
from .models import Quest, EventType, Event

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse


# Unauthenticated Pages ----------------------------------------------------------------


class IndexView(generic.ListView):
    template_name = "questgiver/index.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        """
        All quests with a most recent status of 'Approved' or 'Reposted'
        """
        open_quests = (
            Quest.objects.annotate(latest_event_date = Max('event__created_at'))
            .filter(
                Q(event__created_at=F('latest_event_date')),
                Q(event__event_type=EventType.APPROVE.name)
                | Q(event__event_type=EventType.REPOST.name)
            )
        )
        return sorted(open_quests, key=lambda x: x.sort_order())


class DetailView(generic.DetailView):
    model = Quest
    template_name = "questgiver/detail.html"

    def get_queryset(self):
        """
        All quests with a most recent status of 'Approved' or 'Reposted'
        """
        return (
            Quest.objects.annotate(latest_event_date = Max('event__created_at'))
            .filter(
                Q(event__created_at=F('latest_event_date')),
                Q(event__event_type=EventType.APPROVE.name)
                | Q(event__event_type=EventType.REPOST.name)
            )
        )


def request_new(request):
    return render(request, "questgiver/request.html")


# Authenticated Pages ------------------------------------------------------------------


class PendingView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/pending.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        """
        All quests that have not been 'Approved'
        """
        return Quest.objects.exclude(event__event_type=EventType.APPROVE.name).order_by(
            "-created_at"
        )


class ReviewView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/review.html"


class ReviewOverdueView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/review.html"


class AdjustView(LoginRequiredMixin, generic.DetailView):
    model = Quest
    template_name = "questgiver/adjust.html"


class OverdueView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/overdue.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        """
        All quests with a most recent status of 'Accepted' that is marked overdue
        """
        accepted_requests = (
            Quest.objects.annotate(latest_event_date = Max('event__created_at'))
            .filter(
                event__created_at=F('latest_event_date'),
                event__event_type=EventType.ACCEPT.name
            )
        )
        return [q for q in accepted_requests if q.is_overdue()]


class AbandonedView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/abandoned.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        """
        All quests with a most recent status of 'Abandoned'
        """
        return (
            Quest.objects.annotate(latest_event_date = Max('event__created_at'))
            .filter(
                event__created_at=F('latest_event_date'),
                event__event_type=EventType.ABANDON.name
            )
        )


class CompletedView(LoginRequiredMixin, generic.ListView):
    template_name = "questgiver/completed.html"
    context_object_name = "quest_list"

    def get_queryset(self):
        """
        All quests with a most recent status of 'Completed'
        """
        return (
            Quest.objects.annotate(latest_event_date = Max('event__created_at'))
            .filter(
                event__created_at=F('latest_event_date'),
                event__event_type=EventType.COMPLETE.name
            )
        )


# Unauthenticated Redirects ------------------------------------------------------------


def accept_opportunity(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    if quest.status() == EventType.ACCEPT.name:
        message = "already_accepted"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    quest.accepted_by_email = request.POST["email"]
    quest.accepted_by_phone = request.POST["phone"].replace("-", "")
    acceptance_event = Event(quest=quest, event_type=EventType.ACCEPT.name)
    message = "accepted"
    if acceptance_email(quest):
        try:
            quest.save(event=acceptance_event)
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
    if quest.status() == EventType.COMPLETE.name:
        message = "already_completed"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    if quest.email_code == code:
        completed_event = Event(quest=quest, event_type=EventType.COMPLETE.name)
        message = "completed"
        try:
            quest.save(event=completed_event)
        except Exception as exc:
            logging.error(exc)
            message = "error"
        completed_email(quest)
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def email_abandon_response(request, pk, code):
    quest = get_object_or_404(Quest, pk=pk)
    message = "unverified"
    if quest.status() == EventType.COMPLETE.name:
        message = "already_completed"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    if quest.email_code == code:
        abandoned_event = Event(quest=quest, event_type=EventType.ABANDON.name)
        message = "abandoned"
        try:
            quest.save(event=abandoned_event)
        except Exception as exc:
            logging.error(exc)
            message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


# Authenticated Redirects --------------------------------------------------------------


def approve_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.status() == EventType.APPROVE.name:
        message = "already_approved"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    approved_event = Event(quest=quest, event_type=EventType.APPROVE.name)
    message = "approved"
    try:
        quest.save(event=approved_event)
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def retire_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.status() == EventType.CLOSE.name:
        message = "already_retired"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    closed_event = Event(quest=quest, event_type=EventType.CLOSE.name)
    message = "retired"
    try:
        quest.save(event=closed_event)
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
    adjustment_event = Event(quest=quest, event_type=EventType.ADJUST.name)
    message = "adjusted"
    try:
        quest.save(event=adjustment_event)
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


def repost_request(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    if quest.status() == EventType.REPOST.name:
        message = "already_reposted"
        return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))
    reposted_quest = Quest(
        id=quest.id,
        created_at=quest.created_at,
        updated_at=quest.updated_at,
        contact_name=quest.contact_name,
        contact_email=quest.contact_email,
        contact_phone=quest.contact_phone,
        topic=quest.topic,
        description=quest.description,
        days_allowed=quest.days_allowed,
        priority=quest.priority,
    )
    reposted_event = Event(quest=quest, event_type=EventType.REPOST.name)
    message = "reposted"
    try:
        reposted_quest.save(event=reposted_event)
    except Exception as exc:
        logging.error(exc)
        message = "error"
    return HttpResponseRedirect(reverse("questgiver:message", args=(message,)))


# Utilities ----------------------------------------------------------------------------


def message(request, message):
    return render(request, "questgiver/message.html", {"message": message})
