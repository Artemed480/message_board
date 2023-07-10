from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Reply

@receiver(post_save, sender=Reply)
def notify_user_about_reply(sender, instance, created, **kwargs):
    if created:
        mail_subject = f'{instance.replier} оставил отклик на ваше объявление "{instance.announce}"'
        to_email = instance.announce.author.email
        html_content = render_to_string(
            'announces/notify_about_reply.html',
            {
                'instance': instance,
            }
        )

    else:
        if instance.accept:
            mail_subject = f'{instance.announce.author} принял ваш отклик на объявление "{instance.announce}"'
            to_email = instance.replier.email
            html_content = render_to_string(
                'announces/notify_about_accept_reply.html',
                {
                    'instance': instance,
                }
            )


    email = EmailMultiAlternatives(
        mail_subject,
        instance.content,
        from_email='Tchesnokov.4lexander@yandex.ru',
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()