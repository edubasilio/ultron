from django.utils import timezone
from haystack import indexes

from .models import Recorte


class RecorteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    data_modificacao = indexes.DateTimeField(model_attr='data_modificacao')
    numeracao_unica = indexes.CharField(model_attr='numeracao_unica')
    codigo_diario = indexes.CharField(model_attr='codigo_diario')
    caderno = indexes.CharField(model_attr='caderno')

    def get_model(self):
        return Recorte

    # def index_queryset(self, using=None):
    #     return self.get_model().objects.filter(data_modificacao__lte=datetime.datetime.now())
    
    def index_queryset(self, pk, using=None):
        return self.get_model().objects.get(id=pk)
