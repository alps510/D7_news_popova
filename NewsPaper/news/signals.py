from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory, UserCategory
from .tasks import notify_subscribers


@receiver(m2m_changed, sender=Post.category.through)
def post_add_signal(instance, action, **kwargs):
    instance_id = instance.id
    if action == 'post_add':
        notify_subscribers.delay(instance_id)


