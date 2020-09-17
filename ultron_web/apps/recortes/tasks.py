import math
from django.utils import timezone

from celery import shared_task

from .models import Recorte
from config.models import RecorteQueryConfig


# @shared_task
# def sample_task():
#     print("!!!! The sample task just ran!!!!")

@shared_task
def get_recortes(loops=math.inf):
    rqc = RecorteQueryConfig.objects.last()
    last_indexing_moment = rqc.last_indexing_moment
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
        # remove recortes q não foram modificados
        last_indexing_moment = timezone.datetime.now()
        _recortes = [r for r in _recortes if timezone.make_naive(r.get('data_modificacao')) > last_indexing_moment]

        if r_len < limit:
            break
    
    rqc.offset = offset
    rqc.last_indexing_moment = last_indexing_moment
    rqc.save()
