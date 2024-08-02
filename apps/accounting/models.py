from django.db import models

from apps.inventory.models import Product

# Create your models here.


class Accounting(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    last_transaction = models.DateTimeField(auto_now=True)
    last_transaction_amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    last_transaction_type = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Accounting'
        ordering = ['last_transaction']

    def __str__(self):
        return f'Accounting: {self.current_balance}'
