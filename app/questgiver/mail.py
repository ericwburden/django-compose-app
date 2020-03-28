import os

from .models import Quest

from django.core.mail import send_mail
from django.template.loader import render_to_string


def acceptance_email(quest: Quest):
    params = {
        "topic": quest.topic,
        "description": quest.description,
        "days": quest.days_allowed,
        "contact_name": quest.contact_name,
        "contact_email": quest.contact_email,
        "contact_phone": quest.contact_phone,
        "server_name": os.getenv("SERVER_HOSTNAME", default="localhost"),
        "id": quest.id,
        "code": quest.email_code,
    }

    msg_plain = render_to_string("questgiver/emails/acceptance.txt", params)
    msg_html = render_to_string("questgiver/emails/acceptance_inline.html", params)

    return send_mail(
        "Opportunity Accepted!",
        msg_plain,
        os.getenv("EMAIL_SENDER", default="name@example.org"),
        [quest.accepted_by_email],
        html_message=msg_html,
    )


def accepted_email(quest: Quest):
    params = {
        "topic": quest.topic,
        "description": quest.description,
        "accepted_by_email": quest.accepted_by_email,
        "accepted_by_phone": quest.accepted_by_phone,
    }

    msg_plain = render_to_string("questgiver/emails/accepted.txt", params)
    msg_html = render_to_string("questgiver/emails/accepted_inline.html", params)

    return send_mail(
        f"{quest.topic} | Accepted",
        msg_plain,
        os.getenv("EMAIL_SENDER", default="name@example.org"),
        [quest.contact_email],
        html_message=msg_html,
    )


def completed_email(quest: Quest):
    params = {
        "topic": quest.topic,
        "description": quest.description,
        "accepted_by_email": quest.accepted_by_email,
        "accepted_by_phone": quest.accepted_by_phone,
    }

    msg_plain = render_to_string("questgiver/emails/completed.txt", params)
    msg_html = render_to_string("questgiver/emails/completed_inline.html", params)

    return send_mail(
        f"{quest.topic} | Reported Complete",
        msg_plain,
        os.getenv("EMAIL_SENDER", default="name@example.org"),
        [quest.contact_email],
        html_message=msg_html,
    )
