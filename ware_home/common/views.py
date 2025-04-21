from urllib.parse import urlencode

from django.views.generic import RedirectView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class QrCodeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        base_url = self.url

        kwargs = self.kwargs

        query_args = {
            "bar_code": kwargs["bar_code"],
            "supply_id": kwargs["supply_id"],
        }

        query_string = urlencode(query_args)

        base_url = f"{base_url}?{query_string}"

        return base_url


class HealthCheckView(APIView):
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(200)
