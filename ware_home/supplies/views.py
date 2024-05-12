from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


class ScannerPocView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "scanner/scanner_poc.html"

    def test_func(self):
        return self.request.user.is_staff
