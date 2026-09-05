import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("cire")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()
app.autodiscover_tasks(
    [
        "apps.experiments.async_bench",
        # "apps.experiments.caching_bench",   
        # "apps.experiments.database_bench",  
    ]
)