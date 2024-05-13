from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


class ScannerPocView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "scanner/scanner_poc.html"

    def test_func(self):
        return self.request.user.is_staff


class DispatchView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dispatch/dispatch.html"

    def test_func(self):
        return self.request.user.is_staff


class AddStockView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "add-stock/add-stock.html"

    def test_func(self):
        return self.request.user.is_staff


class PopStockView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "pop-stock/pop-stock.html"

    def test_func(self):
        return self.request.user.is_staff


class StockListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "stock/stock-list.html"

    def test_func(self):
        return self.request.user.is_staff
