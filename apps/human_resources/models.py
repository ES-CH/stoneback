from django.db import models

from apps.inventory.models import CommonModel


class Employee(CommonModel):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name
