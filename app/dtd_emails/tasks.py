# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from dtd_request.models import Request, Response

from django.core.mail import send_mail
from django.template.loader import render_to_string

import os


@shared_task
def test_email(name: str):
    msg_plain = f'Hey, {name}, here\'s your email!'

    return send_mail(
        "Now is your Test!",
        msg_plain,
        os.getenv("EMAIL_SENDER", default="name@example.org"),
        ['eric.w.burden@gmail.com']
    )


@shared_task
def status_update_email(id: int):
    response = Response.objects.get(pk=id)
    msg = {
        "PENDING": (
            "This means it has not yet been picked up by one of our team members for "
            "review. Due to the high volume of requests, we ask for you patience as "
            "we diligently address each request in the order it is received."
        ),
        "RECEIVED": (
            "This means one of our team members has received your request and has been "
            "assigned to review the information you provided. You should expect to hear "
            "from one of our team members within the next 48 hours."
        ),
        "REVIEWED": (
            "This means one of our team members has reviewed the information you have "
            "provided and is currently researching the best options for agencies to "
            "connect you to. Expect to hear from one of our team members within 24 "
            "hours to discuss these options with you."
        ),
        "CONTACTED": (
            "This means one of our team members has already contacted you regarding this "
            "request. Our team member is diligently working to finalize the results from "
            "your call."
        ),
        "REFERRED": (
            "This means you have been referred to one of our network of agencies for "
            "services. Please be patient as our partner agencies are experiences high "
            "volumes of requests at this time."
        ),
        "CLOSED": (
            "This means your request has been closed, either due to connecting you to "
            "one of our partner agencies or because we could not connect you for some "
            "reason. Please feel free to reach out to Driving the Dream if you need "
            "additional assistance with this request."
        )
    }[response.status]

    closing = ""
    if not response.status == 'CLOSED':
        closing += (
            "You can continue to check the status of your request on our web site "
            f"using your phone number ({response.request.primary_phone}) and "
            f"confirmation code ({response.request.confirmation_code})."
        )

    params = {
        "status": response.status,
        "msg": msg,
        "note": response.note,
        "closing": closing,
    }

    msg_plain = render_to_string("dtd_emails/status_update.txt", params)
    msg_html = render_to_string("dtd_emails/status_update_inline.html", params)

    return send_mail(
        "Driving the Dream Update",
        msg_plain,
        os.getenv("EMAIL_SENDER", default="name@example.org"),
        [response.request.email],
        html_message=msg_html,
    )