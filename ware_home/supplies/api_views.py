from django.db.models import Count, F, Sum
from rest_framework import generics, status, views
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ware_home.supplies.models import DemandTag, Product, Supply
from ware_home.supplies.serializers import (
    DemandHASerializer,
    DemandTagSummarySerializer,
    ProductSerializer,
    SupplyPopSerializer,
    SupplySerializer,
)


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


class SupplyFilterApiView(generics.ListAPIView):
    serializer_class = SupplySerializer
    queryset = Supply.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            self.queryset.prefetch_product()
            .annotate_expiration_state()
            .filter(product__bar_code=self.kwargs["bar_code"])
            .order_by(F("expiration_date").asc(nulls_last=True))
        )


class SupplyPopApiView(views.APIView):
    serializer_class = SupplyPopSerializer
    queryset = Supply.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs["id"])

    def post(self, request, *args, **kwargs):
        # Allows both increment and decrementing supply amount
        instance = self.get_object()
        serializer = self.serializer_class(
            data=request.data, context={"instance": instance}
        )
        serializer.is_valid(raise_exception=True)

        instance.amount -= serializer.validated_data["amount_to_pop"]

        if instance.amount == 0:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.save()
        return Response(
            SupplySerializer(instance=instance).data, status=status.HTTP_200_OK
        )


class DemandSummaryView(ListAPIView):
    queryset = DemandTag.objects.none()
    serializer_class = DemandTagSummarySerializer
    authentication_classes = []
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        qs = (
            DemandTag.objects.all()
            .prefetch_related("products")
            .prefetch_related("products__supplies")
        )
        qs = qs.annotate(
            count_in_stock=Sum("products__supplies__amount", default=0)
        ).filter(count_in_stock__lt=F("min_amount"))

        return qs


class DemandSummaryHAView(RetrieveAPIView):
    serializer_class = DemandHASerializer
    authentication_classes = []
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        qs = (
            DemandTag.objects.all()
            .prefetch_related("products")
            .prefetch_related("products__supplies")
        )
        qs = qs.annotate(
            count_in_stock=Sum("products__supplies__amount", default=0)
        ).filter(count_in_stock__lt=F("min_amount"))

        return qs

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance={"demand": self.get_queryset()})
        return Response(serializer.data)
