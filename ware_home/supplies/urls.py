from django.urls import path

from .views import (
    AddStockView,
    DemandView,
    DispatchView,
    PopStockView,
    ScannerPocView,
    StockListView,
)

urlpatterns = [
    path("scanner-poc/", ScannerPocView.as_view(), name="scanner-poc"),
    path("dispatch/", DispatchView.as_view(), name="dispatch"),
    path("add-stock/", AddStockView.as_view(), name="stock-add"),
    path("pop-stock/", PopStockView.as_view(), name="stock-pop"),
    path("stock-list/", StockListView.as_view(), name="stock-list"),
    path("demand/", DemandView.as_view(), name="demand"),
]
