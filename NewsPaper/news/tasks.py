from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from .models import PostCategory, UserCategory, Post


@shared_task
def notify_subscribers(new_post_id, **kwargs):
    rec_list = []
    print(new_post_id)
    print('Hello from task')

    ctgs = PostCategory.objects.filter(post_id=new_post_id)
    for k in ctgs:
        user_ctgs = UserCategory.objects.filter(category_id=k.category_id)
        for u in user_ctgs:
            if User.objects.get(id=u.user_id).email not in rec_list:
                rec_list.append(User.objects.get(id=u.user_id).email)

    send_mail(
        subject=Post.objects.get(id=new_post_id).title,
        message=Post.objects.get(id=new_post_id).preview() + f'http://127.0.0.1:8000/posts/{new_post_id}',
        from_email='alps51@yandex.ru',
        recipient_list=rec_list,
    )


@shared_task()
def monday_post():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    post_list = Post.objects.filter(date__lte=end_date, date__gte=start_date)
    rec_list_id = UserCategory.objects.all().values('user_id').distinct()
    # все подписавшиеся
    rec_list = []
    for rec in rec_list_id:
        rec_list.append(User.objects.filter(id=rec['user_id'])[0].email)

    html_content = render_to_string('account/email/weekly_post.html',
                                    {'posts': post_list, }, )
    msg = EmailMultiAlternatives(
        subject='Новости этой недели',
        body='',
        from_email='alps51@yandex.ru',
        to=rec_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
