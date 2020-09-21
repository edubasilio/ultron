import math
from django.utils import timezone

from celery import shared_task

from .models import Recorte
from config.models import RecorteQueryConfig


@shared_task
def send_recortes_to_es(recortes):
    print("-------------------------------")
    print("--- Recortes:", len(recortes))
    return recortes

@shared_task
def get_recortes_from_db_task(loops=math.inf):
    rqc = RecorteQueryConfig.objects.last()
    rqc = RecorteQueryConfig.objects.create() if rqc is None else rqc
    last_indexing_moment = rqc.last_indexing_moment
    begin_moment = timezone.datetime.now()
    offset = rqc.offset
    limit = rqc.limit
    
    recortes = Recorte.objects.all().values('id','data_modificacao')
    n = 0

    while n < loops:
        n = n + 1
        print(n)

        _limit = offset + limit
        _recortes = list(recortes[offset:_limit])
        offset = _limit + 1
        r_len = len(_recortes)
        print(_recortes[0])
        
        print("@@@ Recortes:", len(_recortes))
        # remove recortes q não foram modificados
        _recortes = [r for r in _recortes if r.get('data_modificacao') > last_indexing_moment]
        print("### Recortes:", len(_recortes))

        # envia _recortes para rabbitmq
        if len(_recortes) > 0:
            send_recortes_to_es.apply_async((_recortes,), ignore_result=True)

        if r_len < limit:
            break
    
    rqc.offset = offset
    rqc.last_indexing_moment = begin_moment
    rqc.save()
