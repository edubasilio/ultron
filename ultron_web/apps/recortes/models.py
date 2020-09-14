from django.utils.translation import gettext as _
from django.db import models

# Create your models here.
class Recorte(models.Model):
    data_criacao = models.DateField(verbose_name=_('Data de Criação'))
    data_modificacao = models.DateTimeField(verbose_name=_('Data de Modificação'))
    numeracao_unica = models.CharField(max_length=20, verbose_name=_('Numeração Única'))
    recorte = models.TextField(verbose_name=_('Recorte'))
    data_publicacao = models.DateField(verbose_name=_('Data de Publicação'))
    codigo_diario = models.CharField(max_length=200, verbose_name=_('Código Diário'))
    caderno = models.CharField(max_length=200, verbose_name=_('Caderno'))
    novo_recorte = models.BooleanField(verbose_name=_('Novo Recorte'))
    paginas_diario = models.TextField(verbose_name=_('Páginas Diário'))
    nup_invalido = models.BooleanField(verbose_name=_('NUP Inválido'))
    nup_invalido_msg = models.CharField(max_length=120, verbose_name=_('NUP Invalido Mensagem'))

    class Meta:
        verbose_name = _('Recorte')
        verbose_name_plural = _('Recortes')
    
    def __str__(self):
        return f"{self.pk}"
