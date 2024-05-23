from django.urls import path

from .api_views import ProductApiView

urlpatterns = [
    path(
        "product/<str:bar_code>/",
        ProductApiView.as_view(),
        name="product-detail",
    ),
]
