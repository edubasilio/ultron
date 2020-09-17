from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class SingletonModel(models.Model):
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


# Create your models here.
class RecorteQueryConfig(SingletonModel):
    offset = models.BigIntegerField(default=0)
    limit = models.IntegerField(default=200000)
    last_indexing_moment = models.DateTimeField(default=timezone.datetime(1970, 1, 1))

    class Meta:
        verbose_name = _('Recorte Query Config')
        verbose_name_plural = _('Recorte Query Config')

    def __str__(self):
        return f"{self.limit}"
