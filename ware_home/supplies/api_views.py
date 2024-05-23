from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated

from ware_home.supplies.models import Category, Product
from ware_home.supplies.serializers import CategorySerializer, ProductSerializer


class ProductApiView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "bar_code"
