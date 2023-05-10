from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField()
    items = models.JSONField()

    def __str__(self):
        return self.cart_id
