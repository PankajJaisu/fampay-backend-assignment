
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fampay_videohub.settings')

app = Celery('fampay_videohub')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'fetch_videos_every_10_seconds': {
        'task': 'youtube_videos.tasks.fetch_videos_task',  
        'schedule': 10.0,  #
    },
}
