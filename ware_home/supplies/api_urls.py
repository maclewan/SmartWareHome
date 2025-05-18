from django.urls import path

from .api_views import (
    DemandSummaryHAView,
    DemandSummaryView,
    ProductCreateApiView,
    ProductDetailApiView,
    SupplyCreateApiView,
    SupplyFilterApiView,
    SupplyPopApiView,
)

urlpatterns = [
    path(
        "product/<str:bar_code>/",
        ProductDetailApiView.as_view(),
        name="product-detail",
    ),
    path(
        "product/",
        ProductCreateApiView.as_view(),
        name="product-create",
    ),
    path(
        "supply/",
        SupplyCreateApiView.as_view(),
        name="supply-create",
    ),
    path(
        "supply/for-product/<str:bar_code>/",
        SupplyFilterApiView.as_view(),
        name="supply-filter-list",
    ),
    path(
        "supply/pop-amount/<int:id>/",
        SupplyPopApiView.as_view(),
        name="supply-pop-amount",
    ),
    path(
        "demand/summary/",
        DemandSummaryView.as_view(),
        name="demand-summary",
    ),
    path(
        "demand/summary/ha/",
        DemandSummaryHAView.as_view(),
        name="demand-summary-ha",
    ),
]
