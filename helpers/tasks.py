import traceback
import os

from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
# from celeryconf import app as celery_app


logger = get_task_logger(__name__)


# @celery_app.task
def send_email(
    subject,
    message,
    email,
    cc=[],
    bcc=[],
    subtype="text",
    fileobj=None,
    remove_file=True,
    from_email=None,
    html_data=None,
):
    try:
        if not isinstance(email, list):
            email = [email]

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        emailmessage = EmailMultiAlternatives(
            subject, message, from_email, email, cc=cc, bcc=bcc
        )

        if subtype == "html":
            emailmessage.content_subtype = "html"

        if html_data:
            emailmessage.attach_alternative(html_data, "text/html")

        if fileobj:
            if not isinstance(fileobj, list):
                fileobj = [fileobj]
            for obj in fileobj:
                fobj = open(obj["filepath"], "rb")
                emailmessage.attach(
                    obj["filename"], fobj.read(), obj.get("mimetype", "")
                )
                if remove_file:
                    os.remove(obj["filepath"])

        emailmessage.send()
    except Exception:
        admin_msg = "Subject: {}\nTo: {}\nFrom: {}\n{}".format(
            subject, email, from_email, traceback.format_exc()
        )
        logger.error(f"Error email enqueue {admin_msg}")
    return True
