import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from datetime import timedelta
from ...models import Post, UserCategory
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    post_list = Post.objects.filter(date__lte=end_date, date__gte=start_date)
    rec_list_id = UserCategory.objects.all().values('user_id').distinct()
    #все подписавшиеся
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

    print('hello from job')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")