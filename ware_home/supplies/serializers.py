from rest_framework import serializers

from ware_home.supplies.models import Category, Product, Supply


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class SupplySerializer(serializers.ModelSerializer):
    expiration_state = serializers.CharField(read_only=True)

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
