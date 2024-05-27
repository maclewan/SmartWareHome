from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ware_home.supplies.models import Product, Supply
from ware_home.supplies.serializers import ProductSerializer, SupplySerializer


class ProductDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "bar_code"


class ProductCreateApiView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class SupplyCreateApiView(generics.CreateAPIView):
    serializer_class = SupplySerializer
    queryset = Supply.objects.all()
    permission_classes = [IsAuthenticated]


# todo TESTS
class SupplyFilterApiView(generics.ListAPIView):
    serializer_class = SupplySerializer
    queryset = Supply.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.select_related("product").filter(
            product__bar_code=self.kwargs["bar_code"]
        ).order_by("expiration_date")
