from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from datetime import datetime, timedelta

from announces.models import Announce



DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

def get_emails():
    queryset = User.objects.all()

    user_emails = []
    for user in queryset:
        user_emails.append(user.email)
    print(user_emails)

    return user_emails


def notify_users():
    announces = Announce.objects.filter(pub_date__range=(datetime.now()-timedelta(days=7), datetime.now()))
    user_emails = get_emails()
    html = render_to_string(
        'announces/week_notify.html',
        {
            'announces': announces,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'New post in current week',
        from_email=DEFAULT_FROM_EMAIL,
        body='',
        to=user_emails
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()