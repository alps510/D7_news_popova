import os
from celery import Celery

#связываем настройки Django с настройками Celery через переменную окружения
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

#создаём экземпляр приложения Celery и устанавливаем для него файл конфигурации.
# указываем пространство имён, чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py.
# Он их будет искать по шаблону «CELERY_***»
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

#автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_monday_news': {
        'task': 'news.tasks.monday_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}
