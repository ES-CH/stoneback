from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history import register


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=128, unique=True, error_messages={
                            'unique': _('This company already exists.')})
    nit = models.CharField(max_length=12)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return u'%s' % self.name


register(Company)
