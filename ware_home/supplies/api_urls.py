from django.urls import path

from .api_views import (
    ProductCreateApiView,
    ProductDetailApiView,
    SupplyCreateApiView,
    SupplyFilterApiView,
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
]
