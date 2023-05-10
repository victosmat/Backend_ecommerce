from django.db import models

class Inventory(models.Model):
    
    address = models.CharField(max_length=200)
    book_quantity = models.IntegerField()
    clothes_quantity = models.IntegerField()
    electronics_quantity = models.IntegerField()
    items = models.JSONField()
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.address
