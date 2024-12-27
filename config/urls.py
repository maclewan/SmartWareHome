"""
URL configuration for ware_home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse, reverse_lazy
from django.views.generic import RedirectView

from ware_home.common.views import QrCodeRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("supplies/", include("ware_home.supplies.urls")),
    path("api/supplies/", include("ware_home.supplies.api_urls")),
    path(
        "qr/<str:bar_code>/<str:supply_id>/",
        QrCodeRedirectView.as_view(url=reverse_lazy("stock-pop")),
        name="qr-redirect",
    ),
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("dispatch")),
        name="home-view-redirect",
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    swagger_urls = [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/", SpectacularSwaggerView.as_view()),
    ]

    media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + swagger_urls
