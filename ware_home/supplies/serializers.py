from datetime import date

from rest_framework import serializers

from ware_home.supplies.models import Category, DemandTag, Product, Supply


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    demand_tags = serializers.PrimaryKeyRelatedField(
        queryset=DemandTag.objects.all(), many=True, write_only=True
    )
    demand_tag = serializers.CharField(source="demand_tags.first.id", read_only=True)

    class Meta:
        model = Product
        fields = [
            "bar_code",
            "demand_tags",
            "demand_tag",
            "description",
            "id",
            "name",
            "volume",
            "categories",
        ]


class SupplySerializer(serializers.ModelSerializer):
    expiration_state = serializers.CharField(read_only=True)
    expiration_date = serializers.DateField(default=None, allow_null=True)

    class Meta:
        model = Supply
        fields = [
            "id",
            "created_at",
            "updated_at",
            "amount",
            "expiration_date",
            "product",
            "expiration_state",
        ]


class SupplyPopSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise RuntimeError("This serializer is not ment to create objects.")

    def update(self, instance, validated_data):
        raise RuntimeError("This serializer is not ment to update objects.")

    amount_to_pop = serializers.DecimalField(decimal_places=1, max_digits=5)

    def validate(self, attrs):
        instance = self.context["instance"]
        assert instance is not None
        if attrs["amount_to_pop"] > instance.amount:
            raise serializers.ValidationError(
                {"amount_to_pop": "Cannot pop more amount that in stock."}
            )
        return attrs


class ProductFilterViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDemandSummarySerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = [
            "id",
            "bar_code",
            "name",
            "volume",
        ]


class DemandTagSummarySerializer(serializers.ModelSerializer):
    products = ProductDemandSummarySerializer(many=True, read_only=True)
    count_in_stock = serializers.DecimalField(
        decimal_places=2, max_digits=10, read_only=True
    )

    class Meta:
        model = DemandTag
        fields = ["name", "id", "min_amount", "count_in_stock", "products"]


class DemandHASerializer(serializers.Serializer):
    demand = DemandTagSummarySerializer(many=True)
