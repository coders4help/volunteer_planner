import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volunteer_planner.settings.local")

app = Celery()
app.config_from_object("django.conf:settings", namespace="CELERY", force=True)
app.autodiscover_tasks()
