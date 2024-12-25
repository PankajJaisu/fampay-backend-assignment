# fampay_videohub/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fampay_videohub.settings')

# Create Celery application instance
app = Celery('fampay_videohub')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover and register tasks from all registered Django apps
app.autodiscover_tasks()

# Optional: You can configure periodic tasks here

app.conf.beat_schedule = {
    'fetch_videos_every_10_seconds': {
        'task': 'youtube_videos.tasks.fetch_videos_task',  # Call the task defined in youtube_videos/tasks.py
        'schedule': 10.0,  # Run every 10 seconds
    },
}
