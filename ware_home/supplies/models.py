from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=127)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    volume = models.CharField(max_length=127, null=True, blank=True)
    categories = models.ManyToManyField(Category)


class Supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=1, max_digits=5)
