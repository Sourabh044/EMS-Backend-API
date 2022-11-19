from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def leave_apply_email(request, user, leave, mail_subject, template_name):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = request["get_host"]
    mail_subject = mail_subject
    print(leave.date)
    html_message = render_to_string(
        template_name,
        {
            "user": user,
            "leave": leave,
            "domain": current_site,
        },
    )
    text_message = strip_tags(html_message)
    to_email = user.email
    mail = EmailMessage(mail_subject, html_message, from_email, to=[to_email])
    mail = EmailMultiAlternatives(mail_subject, text_message, from_email, to=[to_email])
    mail.attach_alternative(html_message, "text/html")
    mail.send()
