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
    categories = models.ManyToManyField(Category, blank=True)

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

    def schedule_for_print(self):
        self.update(scheduled_print=True)
        return self

    def un_schedule_for_print(self):
        self.update(scheduled_print=False)
        return self

    def prefetch_product(self):
        return self.select_related("product")

    def scheduled_for_print(self):
        return self.filter(scheduled_print=True).prefetch_product()

    def not_printed(self):
        return self.filter(printed_once=False)

    def mark_as_printed(self):
        self.update(scheduled_print=False, printed_once=True)
        return self


class Supply(TimeStampModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="supplies"
    )
    amount = models.DecimalField(decimal_places=1, max_digits=5)
    expiration_date = models.DateField(null=True, blank=True, default=None)
    printed_once = models.BooleanField(default=False)
    scheduled_print = models.BooleanField(default=False)

    objects = SupplyQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "supplies"

    def __str__(self):
        return f"Supply #{self.id} {self.product.name}"


class DemandTag(models.Model):
    min_amount = models.DecimalField(decimal_places=1, max_digits=5)
    name = models.CharField(max_length=63)
    # following could and should be just a FK, but m2m was used to make admin impl easier
    products = models.ManyToManyField(Product, related_name="demand_tags", blank=True)

    def __str__(self):
        return f"Tag #{self.id} {self.name}"
