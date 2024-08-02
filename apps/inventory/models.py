from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CommonModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(CommonModel):
    name = models.CharField(max_length=128, unique=True, error_messages={
                            'unique': _('This company already exists.')})
    nit = models.CharField(max_length=12)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return u'%s' % self.name


class Product(CommonModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name


class Inventory(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return u'%s' % self.product.name
