import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import (
    Case,
    DurationField,
    ExpressionWrapper,
    F,
    IntegerField,
    Min,
    Value,
    When,
)
from django.db.models.functions import Cast
from django.utils import timezone
from django.views.generic import TemplateView

from ware_home.common.views import XFrameOptionsExemptMixin
from ware_home.supplies.models import Category, DemandTag, Product
from ware_home.supplies.serializers import (
    DemandTagSummarySerializer,
    ProductFilterViewSerializer,
)


class ScannerPocView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "scanner/scanner.html"

    def test_func(self):
        return self.request.user.is_staff


class DispatchView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dispatch/dispatch.html"

    def test_func(self):
        return self.request.user.is_staff


class AddStockView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "add-stock/add_stock.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("name")
        context["demand_tags"] = DemandTag.objects.all()
        return context


class PopStockView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "pop-stock/pop_stock.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("name")
        return context


class StockListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "stock/stock-list.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products_qs = (
            Product.objects.filter(supplies__isnull=False)
            .distinct()
            .prefetch_related("categories")
        )

        context["categories"] = Category.objects.all().order_by("name")
        context["products"] = self._get_aggregated_products(products_qs)
        context["products_json"] = json.dumps(
            ProductFilterViewSerializer(products_qs, many=True).data
        )
        return context

    def _get_aggregated_products(self, products_qs):
        return (
            products_qs.annotate_supplies_sum()
            .annotate(closes_expiration_date=Min("supplies__expiration_date"))
            .annotate(
                days_to_closes_expiration_date=Cast(
                    ExpressionWrapper(
                        F("closes_expiration_date") - timezone.now().date(),
                        output_field=DurationField(),
                    )
                    / timezone.timedelta(days=1),
                    output_field=IntegerField(),
                )
            )
            .annotate(
                expiration_row_class_name=Case(
                    When(
                        days_to_closes_expiration_date__lte=1, then=Value("expired-row")
                    ),
                    When(
                        days_to_closes_expiration_date__lte=15,
                        then=Value("soon-to-expire-row"),
                    ),
                    default=Value(""),
                )
            )
            .order_by(F("days_to_closes_expiration_date").asc(nulls_last=True))
        )


class DemandView(XFrameOptionsExemptMixin, TemplateView):
    template_name = "demand/demand.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demand"] = DemandTagSummarySerializer(
            instance=DemandTag.objects.demand_summary(), many=True
        ).data
        return context
