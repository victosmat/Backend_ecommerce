from __future__ import unicode_literals
from django.db import models

# Create your models here.

class cart(models.Model):
    username = models.CharField(max_length=200)
    product_id = models.CharField(max_length=10)
    quantity = models.CharField(max_length=5)
    status = models.CharField(max_length=15)

    def __str__(self):
        return '%s %s %s %s' % (self.username, self.product_id, self.quantity, self.status)
