"""Posts models."""

# Django
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=150)


class Category(models.Model):
    name = models.CharField(max_length=150)


class Sku(models.Model):
    reference = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)


class Item(models.Model):
    gross = models.FloatField()
    discounts = models.FloatField()
    subtotal = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    # sku = models.ManyToManyField(Sku)
    sku = models.ForeignKey(
        Sku, on_delete=models.CASCADE)


class Customer(models.Model):
    document_type = models.CharField(max_length=25)
    document_number = models.PositiveIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=100)


class Invoice(models.Model):
    createtime = models.DateTimeField()
    document_number = models.CharField(max_length=16)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    # item = models.ForeignKey(
    #     Item, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.document_number

