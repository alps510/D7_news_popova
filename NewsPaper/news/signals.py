from django.db.models.signals import m2m_changed ,post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, PostCategory, UserCategory, User


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(instance, action, **kwargs):
    rec_list = []
    if action == 'post_add':
        ctgs = PostCategory.objects.filter(post_id=instance.id)
        for k in ctgs:
            user_ctgs = UserCategory.objects.filter(category_id=k.category_id)
            for u in user_ctgs:
                if User.objects.get(id=u.user_id).email not in rec_list:
                    rec_list.append(User.objects.get(id=u.user_id).email)
    print(rec_list)

    send_mail(
        subject=instance.title,
        message=instance.preview() + f'http://127.0.0.1:8000/posts/{instance.pk}',
        from_email='alps51@yandex.ru',
        recipient_list=rec_list,
    )

