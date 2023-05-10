from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.address


class FullName(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Customer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    full_name = models.ForeignKey(FullName, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name.first_name + ' ' + self.full_name.last_name
