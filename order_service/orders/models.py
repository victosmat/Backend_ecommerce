from django.db import models

class Order(models.Model):
    user_id = models.IntegerField()
    description = models.JSONField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)
