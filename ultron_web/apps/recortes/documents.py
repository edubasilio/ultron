from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Recorte


@registry.register_document
class RecorteDocument(Document):
    class Index:
        name = 'recortes'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Recorte
        fields = [
            'id',
            'data_criacao',
            'data_modificacao',
            'numeracao_unica',
            'recorte',
            'data_publicacao',
            'codigo_diario',
            'caderno',
            'paginas_diario'
        ]
