from django.db import models

from ware_home.common.models import TimeStampModel


class Category(models.Model):
    name = models.CharField(max_length=127)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"Category #{self.id} {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    bar_code = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    volume = models.CharField(max_length=127, null=True, blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"Product #{self.id} {self.name}"


class Supply(TimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=1, max_digits=5)
    expiration_date = models.DateField()

    class Meta:
        verbose_name_plural = "supplies"

    def __str__(self):
        return f"Supply #{self.id} {self.product.name}"
