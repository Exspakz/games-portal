from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Comment


@receiver(post_save, sender=Comment)
def notify_user_post(sender, instance, created, **kwargs):

    site = Site.objects.get_current()
    site_name = site.name

    template = None
    first_name = None
    title_post = instance.post.title
    text_comment = instance.text
    link_post = f'http://{site.domain}:8000/{instance.post.id}'

    subject = None
    email = None

    if created:
        print('Hello, I am a created comment!!!')

        user = instance.post.user
        template = 'email_notify_about_new_comment.html'
        first_name = user.first_name if user.first_name else user.username

        subject = f'{site_name}! New commentary on your post'
        email = user.email

    if instance.is_accept:
        print('Hello, I am a accepted comment!!!')

        user = instance.user
        template = 'email_notify_about_accepted_comment.html'
        first_name = user.first_name if user.first_name else user.username

        subject = f'{site_name}! Your commentary on the post was accepted'
        email = user.email

    html_content = render_to_string(
        f'email/{template}',
        {
            'name': first_name,
            'text_comment': text_comment,
            'title_post': title_post,
            'site_name': site_name,
            'link': link_post,
        }
    )

    message = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    message.attach_alternative(html_content, 'text/html')
    message.send()
