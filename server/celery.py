from __future__ import absolute_import
import os
from celery import Celery
from .tasks import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
app = Celery("server")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-5-minute': {
        'task': 'server.tasks.jobs_cleaner',
        'schedule': 60*60*24,
    },
}
app.conf.timezone = 'UTC'
