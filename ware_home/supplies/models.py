from django.db import models
from django.db.models import (
    Case,
    DurationField,
    ExpressionWrapper,
    F,
    IntegerField,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Cast
from django.utils import timezone

from ware_home.common.models import TimeStampModel


class Category(models.Model):
    name = models.CharField(max_length=127)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"Category #{self.id} {self.name}"


class ProductQuerySet(models.QuerySet):
    def annotate_supplies_sum(self):
        return self.annotate(supplies_sum=Sum("supplies__amount"))


class Product(models.Model):
    name = models.CharField(max_length=255)
    bar_code = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    volume = models.CharField(max_length=127, null=True, blank=True)
    categories = models.ManyToManyField(Category)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return f"Product #{self.id} {self.name}"


class SupplyQuerySet(models.QuerySet):
    def annotate_days_to_expiration(self):
        return self.annotate(
            days_to_expiration=Cast(
                ExpressionWrapper(
                    F("expiration_date") - timezone.now().date(),
                    output_field=DurationField(),
                )
                / timezone.timedelta(days=1),
                output_field=IntegerField(),
            )
        )

    def annotate_expiration_state(self):
        qs = self.annotate_days_to_expiration()
        qs = qs.annotate(
            expiration_state=Case(
                When(days_to_expiration__lte=1, then=Value("expired")),
                When(days_to_expiration__lte=15, then=Value("soon_to_expire")),
                default=Value("good"),
            )
        )
        return qs


class Supply(TimeStampModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="supplies"
    )
    amount = models.DecimalField(decimal_places=1, max_digits=5)
    expiration_date = models.DateField()

    objects = SupplyQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "supplies"

    def __str__(self):
        return f"Supply #{self.id} {self.product.name}"


class DemandTag(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="demand_tag"
    )
    amount = models.DecimalField(decimal_places=1, max_digits=5)
