from django.urls import path

from .api_views import ProductCreateApiView, ProductDetailApiView, SupplyCreateApiView

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
]
