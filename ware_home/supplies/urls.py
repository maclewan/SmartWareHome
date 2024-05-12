from django.urls import path

from .views import ScannerPocView

urlpatterns = [
    path("scanner-poc/", ScannerPocView.as_view(), name="scanner-poc"),
]
