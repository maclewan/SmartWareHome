from django.views.generic import RedirectView
from urllib.parse import urlencode


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
