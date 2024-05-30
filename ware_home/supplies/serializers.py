from abc import ABC

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
    class Meta:
        model = Supply
        fields = "__all__"


class SupplyPopSerializer(serializers.Serializer):
    amount_to_pop = serializers.DecimalField(decimal_places=1, max_digits=5)

    def validate(self, attrs):
        instance = self.context["instance"]
        assert instance is not None
        if attrs["amount_to_pop"] > instance.amount:
            raise serializers.ValidationError("Cannot pop more amount that in stock.")
        return attrs
