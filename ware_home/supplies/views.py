from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from ware_home.supplies.models import Product


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
