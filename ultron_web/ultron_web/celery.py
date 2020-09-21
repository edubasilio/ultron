from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ultron_web.settings')

app = Celery('ultron_web')

# all celery-related configuration keys should have a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.task_router = {
#     'recortes.tasks.send': {'queue': 'for_es'}
# }

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
