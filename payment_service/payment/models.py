# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class payment_status(models.Model):
    username = models.CharField(max_length=200)
    order_id = models.CharField(max_length=10, blank=True, null=True)
    product_id = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    quantity = models.CharField(max_length=5)
    mode_of_payment = models.CharField(max_length=20)
    status = models.CharField(max_length=15)

    def __str__(self):
        return '%s %s %s %s %s %s %s ' % (self.username, self._id, self.product_id, self.price, self.quantity, self.mode_of_payment, self.status)
